# AssistantBot
An AI assistant to help answer questions about Maslow 4. This is an experiment.

The assistant uses the contents of [`common_issues.md`](common_issues.md) as context, so the AI can give accurate, Maslow-specific answers to technical questions.

---

## Option 1 — GitHub Pages + Cloudflare Worker (recommended, free, no user API key required)

This is the best option for a shared community deployment. The API key lives in a Cloudflare Worker secret — it is never sent to the browser. Users visit the GitHub Pages site and chat without needing their own key.

### Step 1 — Deploy the Cloudflare Worker

1. Sign up for a free [Cloudflare account](https://dash.cloudflare.com/sign-up).
2. Install Wrangler (Cloudflare's CLI):
   ```bash
   npm install -g wrangler
   wrangler login
   ```
3. Deploy the worker from this repo:
   ```bash
   npx wrangler deploy
   ```
4. Store your OpenAI API key as a secret (this keeps it out of source control):
   ```bash
   npx wrangler secret put OPENAI_API_KEY
   # Paste your key when prompted
   ```
5. Note the worker URL printed after deployment — it looks like `https://maslow-assistant.<your-subdomain>.workers.dev`.
6. *(Optional but recommended)* Lock the worker to only accept requests from your GitHub Pages domain.
   In `wrangler.toml`, uncomment and set:
   ```toml
   [vars]
   ALLOWED_ORIGIN = "https://<your-org>.github.io"
   ```
   Then redeploy with `npx wrangler deploy`.

### Step 2 — Configure GitHub Pages

1. In your GitHub repository, go to **Settings → Secrets and variables → Actions → Variables** (the *Variables* tab, not Secrets).
2. Add a new repository variable:
   - **Name:** `WORKER_URL`
   - **Value:** your worker URL from Step 1 (e.g. `https://maslow-assistant.example.workers.dev`)
3. Go to **Settings → Pages** and set the source to **GitHub Actions**.
4. Push any commit to `main` — the included workflow (`.github/workflows/deploy-pages.yml`) will build and publish the site automatically, injecting the worker URL.
5. Visit your GitHub Pages URL. The API key field is hidden and users can chat immediately.

---

## Option 2 — GitHub Pages (user provides their own API key)

The simplest deployment — no Cloudflare account needed, but each visitor must paste their own OpenAI API key.

**Steps:**
1. Go to your repository **Settings → Pages**.
2. Under *Source*, choose **Deploy from a branch** and select `main` / `(root)`.
3. Save — GitHub will publish the site at `https://<org>.github.io/<repo>/`.
4. Open the page, paste your OpenAI API key into the key field, and start chatting.

> **Note:** Do **not** set `WORKER_URL` — if the placeholder is not replaced, the page automatically falls back to this direct mode.

---

## Option 3 — Self-hosted Flask server

Use this when you want the API key to stay on your own server.

**Requirements:** Python 3.10+

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=your-key-here
python app.py
# Open http://localhost:5000
```

Environment variables (all optional except `OPENAI_API_KEY`):

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | **Required.** Your OpenAI API key. |
| `OPENAI_MODEL` | `gpt-4o-mini` | Model to use. |
| `OPENAI_MAX_TOKENS` | `2048` | Max tokens in the AI response. |
| `PORT` | `5000` | Port to listen on. |
| `FLASK_DEBUG` | `false` | Enable Flask debug mode (dev only). |

