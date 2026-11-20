# AI Automation Intern — Take-home Assignment
## Build an AI Review Insights Copilot for "Kesar & Co."

Thanks for your interest in the **AI Automation Intern** role. This assignment is a small, realistic version of the work you'd do with us: designing an automation that uses an LLM, connects real tools, behaves safely, and is documented well enough that someone else could run it.

We care about **how you think** as much as what you build. A smaller flow that's reliable, honest about its limits, and well-reasoned beats a large flow that half-works.

---

## At a glance

| | |
|---|---|
| **Time box** | About **2–4 hours** of focused work, spread over the 4 days. Expect the first 30 minutes or so to go on account setup, so start there. Please don't spend more than 5 hours. If you reach that, submit what you have. |
| **Deadline** | **4 days** from when you receive this. Your exact deadline is in your invitation email. |
| **Cost to you** | **₹0**. Everything can be done on free tiers (see [`docs/SETUP.md`](docs/SETUP.md)). |
| **Platform** | Your choice: **n8n** (recommended; the n8n Cloud free trial is quickest to set up), Make, or Zapier. You don't have to write code. Code nodes (Python/JS) are welcome but not required. |
| **Help** | [`docs/SETUP.md`](docs/SETUP.md#6-tips-and-common-sticking-points) has tips for the parts people most often get stuck on. |
| **AI tools** | Allowed and encouraged (ChatGPT, Claude, Gemini, Copilot…). Tell us how you used them. |
| **Questions** | You may send **one email with clarifying questions** within the first 48 hours to the address in your invitation. Asking good questions is part of the job. |

---

## The scenario

**Kesar & Co.** is a fictional D2C Ayurvedic skincare brand that sells on Shopify across India. Its store gets about **40 product reviews a day**. Nobody reads them systematically: risky reviews (skin reactions, abuse, personal details posted in public) sit unnoticed, and unhappy customers never get a reply.

Your job is to build a **review insights copilot**: an automation that reads each review, understands it, flags the risky ones for a human, drafts a short **public reply** where one is needed, and gives the team a summary of each run.

> **Scenario date:** treat **20 November 2026** as "today". Each review has a `submitted_at` timestamp. Use it, **not** your computer's clock, for anything date-related.

---

## What's in this repo

```
.
├── README.md                          ← you are here (the brief)
├── data/
│   ├── reviews.json                   ← 20 product reviews to process
│   ├── faq.md                         ← policies + product info: the ONLY source of truth
│   ├── public_reply_guidelines.md     ← rules for public replies to reviews
│   └── brand_voice.md                 ← how replies should sound
├── schemas/
│   └── llm_output.schema.json         ← required structure for the LLM classification output
├── templates/
│   ├── SUBMISSION_README_TEMPLATE.md  ← use this as your submission README
│   ├── test_report_template.md        ← use this for your test results
│   ├── reviews_log_template.csv       ← import into Google Sheets as your "Reviews Log" tab
│   └── run_summary_template.csv       ← import into the same Google Sheet as your "Run Summary" tab
├── scripts/
│   └── send_test_reviews.py           ← optional: posts each review to your webhook
└── docs/
    ├── SETUP.md                       ← free-tier setup for every tool
    └── SUBMISSION.md                  ← exactly what to submit and how
```

---

## What to build

### Flow overview

```
Trigger: loop over data/reviews.json (or a webhook that receives one review at a time)
   │
   ▼
LLM step: classify + extract  ──►  structured JSON (see schemas/llm_output.schema.json)
   │
   ▼
Route
   ├─ safety concern      → "needs human" + a safe holding reply
   ├─ spam                → log only (no reply)
   ├─ negative / question → draft a public reply (facts only from faq.md)
   └─ positive / neutral  → log (a short thank-you is optional)
   │
   ▼
Log EVERY review to the "Reviews Log" tab
   │
   ▼
After the run: add one row to the "Run Summary" tab
```

### Core requirements (must have)

1. **Classify and extract with an LLM.** For every review, return JSON that matches [`schemas/llm_output.schema.json`](schemas/llm_output.schema.json). The output must be valid every time. Your flow should cope (retry, repair or fall back) when the model returns something invalid.
2. **Route every review** along one of the four paths above.
3. **Draft public replies.** For negative reviews and questions, draft a reply that follows [`data/public_reply_guidelines.md`](data/public_reply_guidelines.md) and [`data/brand_voice.md`](data/brand_voice.md), using facts only from [`data/faq.md`](data/faq.md).
4. **Reviews log.** Write one row per review to the **Reviews Log** tab of a Google Sheet (columns in [`templates/reviews_log_template.csv`](templates/reviews_log_template.csv)).
5. **Run summary.** After each run, add one row to the **Run Summary** tab (columns in [`templates/run_summary_template.csv`](templates/run_summary_template.csv)). The numbers (reviews processed, counts by sentiment, spam, needs human, top topics, products with the most negative reviews) must be **counted by your workflow**, not estimated by the LLM. The LLM may write `summary_text`: 3–5 lines for the team.
6. **Human in the loop.** Low-confidence or risky reviews go to a **"needs human"** state (the `needs_human` flag in the log). You decide the threshold and justify it.
7. **Test and iterate.** Run all 20 reviews through your final version (**v2**). Also run an earlier version (**v1**) on at least 8 reviews of your choice, so you can show what you changed and whether it helped. Report results using [`templates/test_report_template.md`](templates/test_report_template.md).

### Business rules the copilot must follow

- **Replies are public.** Never include personal details (order IDs, phone numbers, email addresses, home addresses) in a reply.
- **Product and policy facts come only from [`data/faq.md`](data/faq.md).** If the FAQ doesn't cover it, the copilot doesn't answer. It escalates.
- **No medical advice**, and never repeat or endorse a claim that a product treats or cures anything.
- **Reported reactions always go to a human** ([`faq.md`](data/faq.md) §8).
- **No public promises:** no discounts, coupons, free products or compensation.
- **Reviews are untrusted input.** Instructions written inside a review must never change how your system behaves.
- Replies are **drafts** stored in the log. Nothing gets posted.

### Suggested order of work

You don't need to build everything at once. This order works well:

1. **Set up your accounts** (LLM and Google Sheets) using [`docs/SETUP.md`](docs/SETUP.md). Allow about 30 minutes.
2. **Classify and log:** trigger → LLM classification → Google Sheet. Get 3–4 reviews working first.
3. **Routing and "needs human":** send each review down the right path.
4. **Reply drafting:** add the public-reply step for negative reviews and questions.
5. **Run summary:** count the results and write the summary row.
6. **Run all 20.** Look at what went wrong, improve your prompts and logic, and run again.
7. **Write up** your README and test report, then record your video.

If you're running short of time, stop adding features. Make what you have reliable and explain what's missing.

### Stretch goals (optional, bonus credit)

- Draft replies with an **AI agent** that has tools (for example `search_faq` and `get_product`)
- Reply in the reviewer's language (Hindi / Hinglish)
- Mask personal details in the log as well as the reply
- Track tokens and cost per review
- Retries with backoff for API failures and rate limits
- Anything else you think a real team would value (tell us why)

---

## Product-thinking questions

Answer these in your submission README (≤150 words each). There's no single right answer. We want to see your reasoning.

1. **Auto-post vs. draft:** These replies are public. Which, if any, would you let post automatically, and which need a human? Where would you set the confidence threshold, and why?
2. **Cost:** Estimate the LLM cost per review and per month at 500 reviews/day. Show your maths.
3. **Success metric:** What's the one metric you'd track in week 1 to know this is working? What would make you switch it off?
4. **Failure experience:** A wrong reply is visible to every shopper. When the copilot gets one wrong, what happens, and how do you limit the damage?
5. **Don't automate:** Name one thing in this flow that should stay manual, and why.

---

**Honesty is scored.** A clear "this part doesn't work yet, here's why, here's what I'd try" earns more than hiding a failure.

---

## Rules

- This must be **your own work**. AI assistants are fine; other people are not.
- Use **only the provided fictional data**. Don't connect real customer data or real stores.
- **Never commit API keys or tokens.** Check your workflow export before submitting.
- If you get stuck, **submit what you have** with honest notes on what's missing. Partial, well-explained submissions are reviewed seriously.
- Shortlisted candidates will do a **live session** where they walk through and extend their build.

---

## Next steps

1. Set up your tools → [`docs/SETUP.md`](docs/SETUP.md)
2. Build, test, iterate
3. Submit → [`docs/SUBMISSION.md`](docs/SUBMISSION.md)

Good luck, and have fun with it.
