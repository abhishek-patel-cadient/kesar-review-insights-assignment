# Kesar & Co. Review Insights Copilot — <Your Name>

> Copy this file into your submission as `README.md` and fill in every section. Keep it concise. Bullet points are fine.

## 1. Summary

- What I built (2–3 lines):
- Platform and LLM used:
- Time spent (approx. hours):
- What works / what doesn't:
- Google Sheet link (view access):

## 2. Architecture

Add a screenshot of the full workflow and a short description of each major step or branch.

![workflow](./screenshots/workflow.png)

| Step / node | What it does | Why I designed it this way |
|---|---|---|
| | | |

## 3. Setup — how someone else can run this

1. Accounts/credentials needed (no actual keys!):
2. How to import the workflow:
3. Where to configure environment variables / credentials:
4. How to run the 20 reviews:

## 4. Prompts

Paste your final prompts (classification + reply drafting, and the summary prompt if you use one). Mention model settings (temperature, etc.).

## 5. Key decisions and assumptions

- How I handle low-confidence classifications:
- How each review gets its route (what is decided by the LLM and what by workflow logic):
- How I keep personal details out of public replies:
- How I keep replies grounded in the FAQ:
- How the run-summary numbers are counted:
- Other assumptions:

## 6. Scaling to 500 reviews/day

What would break first, and what would you change? (rate limits, cost, queueing, monitoring, retries…)

## 7. Product-thinking questions (≤150 words each)

1. **Auto-post vs. draft:** These replies are public. Which, if any, would you let post automatically, and which need a human? Where would you set the confidence threshold, and why?
2. **Cost:** Estimate the LLM cost per review and per month at 500 reviews/day. Show your maths.
3. **Success metric:** What's the one metric you'd track in week 1 to know this is working? What would make you switch it off?
4. **Failure experience:** A wrong reply is visible to every shopper. When the copilot gets one wrong, what happens, and how do you limit the damage?
5. **Don't automate:** Name one thing in this flow that should stay manual, and why.

## 8. How I used AI tools

Which AI tools you used while building (e.g., to write prompts, debug, generate code) and where you relied on your own judgment instead.

## 9. If I had one more week

-
