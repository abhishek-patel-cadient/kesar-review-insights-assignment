#!/usr/bin/env python3
"""
Send the Kesar & Co. test reviews to your workflow's webhook, one at a time.

Uses only the Python standard library (Python 3.8+). No pip install needed.

Examples
--------
  # Send all 20 reviews, 5 seconds apart
  python scripts/send_test_reviews.py --url https://your-n8n-host/webhook/product-review

  # Send only a few reviews
  python scripts/send_test_reviews.py --url <WEBHOOK_URL> --only R01,R05,R12

  # Preview what would be sent, without sending
  python scripts/send_test_reviews.py --url <WEBHOOK_URL> --dry-run

  # Add a header (e.g. if your webhook uses header auth)
  python scripts/send_test_reviews.py --url <WEBHOOK_URL> --header "X-Webhook-Secret: abc123"

Each request is an HTTP POST with Content-Type: application/json and the body
set to ONE review object exactly as it appears in data/reviews.json, e.g.:

  {
    "id": "R01",
    "submitted_at": "2026-11-16T08:42:00+05:30",
    "product": "Saffron Glow Face Serum 30 ml",
    "rating": 5,
    "title": "...",
    "text": "...",
    "author_name": "...",
    "verified_buyer": true
  }
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_FILE = Path(__file__).resolve().parent.parent / "data" / "reviews.json"


def parse_args():
    p = argparse.ArgumentParser(description="POST test reviews to a webhook, one by one.")
    p.add_argument("--url", required=True, help="Your workflow's webhook URL")
    p.add_argument("--file", default=str(DEFAULT_FILE), help="Path to reviews.json")
    p.add_argument("--delay", type=float, default=5.0,
                   help="Seconds to wait between reviews (default: 5). Keep this > 0 to respect API rate limits.")
    p.add_argument("--only", default="", help="Comma-separated review IDs to send, e.g. R01,R07")
    p.add_argument("--header", action="append", default=[],
                   help='Extra HTTP header, e.g. "X-Webhook-Secret: abc". Can be repeated.')
    p.add_argument("--timeout", type=float, default=60.0, help="Request timeout in seconds (default: 60)")
    p.add_argument("--dry-run", action="store_true", help="Print what would be sent without sending")
    return p.parse_args()


def load_reviews(path, only):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    reviews = data["reviews"] if isinstance(data, dict) else data
    if only:
        wanted = {x.strip().upper() for x in only.split(",") if x.strip()}
        missing = wanted - {r["id"] for r in reviews}
        if missing:
            sys.exit(f"Unknown review IDs: {', '.join(sorted(missing))}")
        reviews = [r for r in reviews if r["id"] in wanted]
    return reviews


def build_headers(extra):
    headers = {"Content-Type": "application/json; charset=utf-8", "User-Agent": "kesar-test-sender/1.0"}
    for h in extra:
        if ":" not in h:
            sys.exit(f'Bad --header value (expected "Name: value"): {h}')
        name, value = h.split(":", 1)
        headers[name.strip()] = value.strip()
    return headers


def send(url, review, headers, timeout):
    body = json.dumps(review, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(300).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(300).decode("utf-8", errors="replace")
    except Exception as e:  # network errors, timeouts
        return None, str(e)


def main():
    args = parse_args()
    reviews = load_reviews(args.file, args.only)
    headers = build_headers(args.header)

    print(f"Sending {len(reviews)} review(s) to {args.url} (delay {args.delay}s)\n")
    ok = failed = 0
    for i, review in enumerate(reviews, 1):
        label = f"[{i}/{len(reviews)}] {review['id']}  {review['title'][:60]}"
        if args.dry_run:
            print(f"{label}  -> DRY RUN")
            continue
        status, text = send(args.url, review, headers, args.timeout)
        if status and 200 <= status < 300:
            ok += 1
            print(f"{label}  -> {status} OK")
        else:
            failed += 1
            print(f"{label}  -> FAILED ({status}): {text.strip()[:200]}")
        if i < len(reviews):
            time.sleep(args.delay)

    if not args.dry_run:
        print(f"\nDone. {ok} succeeded, {failed} failed.")
        sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
