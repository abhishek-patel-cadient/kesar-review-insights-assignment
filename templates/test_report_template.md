# Test Report — Kesar & Co. Review Insights Copilot

**Candidate name:**
**Platform used:** n8n / Make / Zapier / other: ____
**LLM(s) used:** (provider + model name)

---

## 1. How I decided what "correct" means

Before measuring accuracy, write down your own expected outcome for each review (sentiment + action) **based on `data/faq.md` and `data/public_reply_guidelines.md`**. Explain any judgment calls in 3–5 lines here.

## 2. Results per review

Fill one row per review. "Expected" is your own judgment. For "Action", describe what the flow did (e.g., *reply drafted*, *needs human + holding reply*, *log only*, *spam, no reply*).

v2 (your final version) must cover all 20 reviews. v1 needs at least 8. Put `—` in the v1 columns for reviews you didn't run in v1.

| Review | Expected sentiment | Expected action | v1 sentiment | v1 action | v1 ✅/❌ | v2 sentiment | v2 action | v2 ✅/❌ | Notes |
|---|---|---|---|---|---|---|---|---|---|
| R01 | | | | | | | | | |
| R02 | | | | | | | | | |
| R03 | | | | | | | | | |
| R04 | | | | | | | | | |
| R05 | | | | | | | | | |
| R06 | | | | | | | | | |
| R07 | | | | | | | | | |
| R08 | | | | | | | | | |
| R09 | | | | | | | | | |
| R10 | | | | | | | | | |
| R11 | | | | | | | | | |
| R12 | | | | | | | | | |
| R13 | | | | | | | | | |
| R14 | | | | | | | | | |
| R15 | | | | | | | | | |
| R16 | | | | | | | | | |
| R17 | | | | | | | | | |
| R18 | | | | | | | | | |
| R19 | | | | | | | | | |
| R20 | | | | | | | | | |

## 3. Summary

*n* = the number of reviews you ran in that version (at least 8 for v1, 20 for v2).

| Metric | Prompt v1 | Prompt v2 |
|---|---|---|
| Reviews run (*n*) | | 20 |
| Sentiment accuracy (x / *n*) | | |
| Correct action (x / *n*) | | |
| Valid JSON on first try (x / *n*) | | |
| Reviews sent to "needs human" | | |
| Run-summary numbers match the Reviews Log (yes / no) | | |
| Avg. tokens per review (if tracked) | | |
| Est. cost per review (₹ or $) | | |

## 4. What I changed from v1 to v2, and why

- Change 1:
- Change 2:
- Change 3:

## 5. Failures I could not fix (be honest)

| Review | What goes wrong | Why I think it happens | What I would try next |
|---|---|---|---|
| | | | |
