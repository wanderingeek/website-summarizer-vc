# website-summarizer-vc
Vibe coded website summarizer using free models from Groq. Built with OpenCode coding agent using the hy3-free model on OpenCode Zen. Used Gradio for UI.

## Setup

```bash
git clone git@github.com:wanderingeek/website-summarizer-vc.git
cd website-summarizer-vc

# uv sync creates/uses the .venv automatically; activation is only needed for the python run
uv sync
. .venv/bin/activate

export GROQ_API_KEY="<your-groq-api-key>"

python main.py
```

This opens the Gradio UI at http://localhost:7860. Paste a URL and click **Summarize** to get a 3-5 bullet Markdown summary.
