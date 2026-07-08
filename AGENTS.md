# Agents.md

Project: website-summarizer-vc — a vibe-coded website summarizer using free models from Groq, built with OpenCode.

## Stack
- UI: Gradio (`gr.Blocks`, Textbox + Button + Markdown output)
- AI model: Groq `llama-3.3-70b-versatile` via the `groq` Python SDK
- Scraping: `requests` + `BeautifulSoup` (`beautifulsoup4`)
- Dependency manager: `uv`
- Python: 3.14, venv at `.venv`

## Plan (as implemented in main.py)
1. **Scrape** (`fetch_article`): GET the URL with a browser User-Agent and 20s timeout, raise on HTTP error. Parse with BeautifulSoup; strip `script/style/nav/footer/header/aside`. Prefer text from `<article>`/`<main>`/`<p>`, falling back to `<body>` or full doc. Collapse blank lines, cap at ~12k chars to fit model context. Raise a friendly error on empty/non-200.
2. **Summarize** (`summarize`): read `GROQ_API_KEY` from env (raise if missing); call `groq.Client().chat.completions.create` with a system prompt instructing a concise 3-5 bullet Markdown summary, user prompt = scraped text. Return `choices[0].message.content`.
3. **Gradio UI** (`build_ui`): Textbox (URL) -> Button ("Summarize") -> Markdown (summary). Wire `button.click` and `url.submit` to a `run` wrapper that catches all exceptions and renders them as `**Error:** ...` Markdown. Launch with `demo.launch()`.

## Reasoning / decisions
- Cap scraped text at 12k chars to stay within model context and keep latency/cost low.
- Strip navigation/boilerplate tags before extracting text to improve summary quality.
- Wrap the full pipeline in try/except so the UI never crashes; errors surface as Markdown.
- `url.submit` added so pressing Enter also triggers summarization.
- **uv gotcha:** `uv add` installed deps into a separate environment, not the existing `.venv`. Packages were installed directly into `.venv` with `uv pip install gradio groq beautifulsoup4 requests`. Keep using `uv pip install` (with the venv activated) for this project's deps rather than `uv add`, unless the venv is recreated.

## Run
```
. .venv/bin/activate
python main.py
```
Opens Gradio at http://localhost:7860. `GROQ_API_KEY` must be set in the environment.
