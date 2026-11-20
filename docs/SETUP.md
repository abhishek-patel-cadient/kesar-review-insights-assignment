# Setup Guide (all free tiers)

Everything in this assignment can be done at **zero cost**. Free-tier limits change from time to time. If one option doesn't work for you, pick an alternative and mention it in your README.

> **Security first:** store every API key/token in your platform's **credentials manager** or a local `.env` file. Never paste keys directly into nodes that get exported, and never commit them. `.env` is already in `.gitignore`.

---

## 1. Automation platform (pick one)

| Option | How to get it | Notes |
|---|---|---|
| **n8n Cloud (easiest)** | Free trial at https://n8n.io | Nothing to install. Google sign-in for Sheets is one click, and webhook URLs are public out of the box. Check the trial lasts past your deadline, and past the live round if you're shortlisted. |
| **n8n — self-hosted** | Docker: `docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n` · or Node: `npx n8n` · then open http://localhost:5678 | Free, no limits. Connecting Google Sheets needs your own Google Cloud OAuth client (see §4). |
| **Make** | Free plan at https://www.make.com | Watch the monthly operations limit. Running 20 reviews × several steps × 2 prompt versions adds up. |
| **Zapier** | Free plan at https://zapier.com | Free-plan limits on multi-step workflows may restrict you. Check before committing. |

Docs for n8n: https://docs.n8n.io

**Public URLs:** if an external service ever needs to call *into* your workflow, a locally hosted instance needs a public URL. Use n8n Cloud or a tunnel such as `ngrok` or `cloudflared`. You don't need one to run the sender script below from your own machine against a local n8n.

---

## 2. LLM API (pick one, or mix)

| Option | Where |
|---|---|
| Google Gemini (free tier via AI Studio) | https://aistudio.google.com |
| Groq (free tier, fast open models) | https://console.groq.com |
| OpenRouter (some free models) | https://openrouter.ai |
| OpenAI / Anthropic | Only if you already have credits. Not required. |

You choose the model(s). Mention them and your settings (temperature, etc.) in your README. Using a cheaper/faster model for classification and a stronger one for drafting is a legitimate design choice. Just explain it.

---

## 3. Data files

Fetch these with an HTTP GET request from your workflow:

- Reviews: https://raw.githubusercontent.com/abhishek-patel-cadient/kesar-review-insights-assignment/refs/heads/main/data/reviews.json
- FAQ (the only source of product and policy facts): https://raw.githubusercontent.com/abhishek-patel-cadient/kesar-review-insights-assignment/refs/heads/main/data/faq.md
- Public reply guidelines: https://raw.githubusercontent.com/abhishek-patel-cadient/kesar-review-insights-assignment/refs/heads/main/data/public_reply_guidelines.md
- Brand voice: https://raw.githubusercontent.com/abhishek-patel-cadient/kesar-review-insights-assignment/refs/heads/main/data/brand_voice.md

How you give the FAQ to the model is up to you: pass all of it (it's short), pass only the relevant section, or put it in a vector store. Explain your choice. The key requirement is that replies stay **grounded** in it.

Field reference (each review):

| Field | Meaning |
|---|---|
| `id` | `R##` |
| `submitted_at` | When the review was posted (IST) |
| `product` | The product named on the review |
| `rating` | Star rating, 1–5 |
| `title`, `text` | What the reviewer wrote |
| `author_name` | The reviewer's display name |
| `verified_buyer` | `true` if the store matched the reviewer to an order |

---

## 4. Google Sheets (reviews log + run summary)

1. Create a Google Sheet named **Kesar Reviews** with two tabs. Use File → Import → "Insert new sheet(s)" to bring in each template's column headers:
   - **Reviews Log**: from [`templates/reviews_log_template.csv`](../templates/reviews_log_template.csv). One row per review.
   - **Run Summary**: from [`templates/run_summary_template.csv`](../templates/run_summary_template.csv). One row per run.
2. You may add columns, but keep the existing ones.
3. **Connecting from n8n:** on n8n Cloud, use **Sign in with Google**. On self-hosted n8n you need a Google Cloud OAuth client. Follow https://docs.n8n.io/integrations/builtin/credentials/google/ (about 15–20 minutes).
4. Before submitting, set sharing to **"Anyone with the link can view"**.

---

## 5. Running the 20 reviews

You can trigger your flow in either of two ways:

**A. Loop inside your workflow (simplest):** fetch the reviews URL above and iterate over `reviews[]`.

**B. Webhook + sender script (closest to real life)**

```bash
# Python 3.8+, no extra packages needed
python scripts/send_test_reviews.py --url <YOUR_WEBHOOK_URL>                # all 20, 5s apart
python scripts/send_test_reviews.py --url <YOUR_WEBHOOK_URL> --only R01,R05  # a subset
python scripts/send_test_reviews.py --url <YOUR_WEBHOOK_URL> --dry-run       # preview only
```

Each POST body is one review object exactly as in `data/reviews.json`.

Either is fine. Keep a **delay between reviews** so you don't hit free-tier rate limits on your LLM.

---

## 6. Tips and common sticking points

- **Start with 3–4 reviews, not all 20.** For example, run your loop on the first few items only, or use `--only R01,R02,R03` with the sender script.
- **Getting valid JSON every time.** Keep the classification temperature at or near 0. In n8n, you can attach a **Structured Output Parser** (paste in the schema) to the LLM node, and wrap it in an **Auto-fixing Output Parser**, which asks the model to repair invalid output. Add a simple fallback for when it still fails, for example `sentiment: "neutral"` plus needs human.
- **Count in your workflow, not in the LLM.** Models are unreliable at counting. Work out the run-summary numbers from the classified items, for example with n8n's **Summarize** node or a few lines in a Code node, and then give those numbers to the LLM if you want it to write `summary_text`.
  - If you trigger one review per webhook call, each review is a separate run of your workflow. In that case, build the summary as a small separate workflow that reads the Reviews Log tab (filtered by `prompt_version`) and counts the rows.
- **Enforce hard rules in workflow logic, not only in prompts.** Prompts can be talked around; IF and Code nodes can't. For example, let an IF node on the LLM's flags decide the route, and check a drafted reply for things it must never contain before you save it. Use the prompt for tone and wording.
- **Keeping replies grounded.** Give the reply step the FAQ and the reply guidelines, and tell it what to do when the FAQ has no answer (say the team will follow up). Test it with a question the FAQ can't answer.
- **AI agent (optional).** If you try the agent stretch goal, attach tools to n8n's AI Agent node, for example an HTTP Request tool that fetches `faq.md`. Give each tool a clear name and description. The agent chooses tools based on those descriptions.
- **Rate limits and flaky APIs.** Keep a few seconds between reviews. In n8n, turn on **Retry On Fail** in the settings of your LLM and API nodes.
- **Exporting without secrets.** If your keys are stored as credentials (not typed into node fields), a normal n8n export won't contain them. Search the file anyway before you commit it.
