# AssistantBot
An AI assistant to help answer questions about Maslow 4. This is an experiment.

The assistant uses the contents of [`common_issues.md`](common_issues.md) as context, so the AI can give accurate, Maslow-specific answers to technical questions.

---

## Option 1 — GitHub Pages (static, no server required)

The easiest way to host this. GitHub Pages serves `index.html` directly; the browser calls the OpenAI API on the user's behalf.

**Steps:**
1. Go to your repository **Settings → Pages**.
2. Under *Source*, choose **Deploy from a branch** and select `main` / `(root)`.
3. Save — GitHub will publish the site at `https://<org>.github.io/<repo>/`.
4. Open the page, paste your OpenAI API key into the key field, and start chatting.

> **Note:** The API key is stored only in your browser's `localStorage` and is sent directly to `api.openai.com`. It is never transmitted to any other server.

---

## Option 2 — Self-hosted Flask server

Use this when you want the API key to stay on the server rather than in the browser.

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

