import os

import gradio as gr
import requests
from bs4 import BeautifulSoup
from groq import Groq

MODEL = "llama-3.3-70b-versatile"
MAX_CHARS = 12000
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def fetch_article(url: str) -> str:
    if not url or not url.strip():
        raise ValueError("Please enter a website URL.")

    try:
        resp = requests.get(url.strip(), headers={"User-Agent": USER_AGENT}, timeout=20)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise ValueError(f"Failed to fetch the page: {exc}")

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()

    container = soup.find("article") or soup.find("main") or soup.find("body")
    if container:
        paragraphs = container.find_all("p")
        if paragraphs:
            text = "\n".join(p.get_text(strip=True) for p in paragraphs)
        else:
            text = container.get_text(separator="\n", strip=True)
    else:
        text = soup.get_text(separator="\n", strip=True)

    text = "\n".join(line for line in text.splitlines() if line.strip())
    if not text.strip():
        raise ValueError("Could not extract any readable text from the page.")

    return text[:MAX_CHARS]


def summarize(text: str) -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a concise webpage summarizer. Summarize the provided "
                    "webpage content as 3 to 5 bullet points in Markdown. Focus on the "
                    "key information. Do not include a preamble."
                ),
            },
            {"role": "user", "content": text},
        ],
    )
    return completion.choices[0].message.content


def run(url: str) -> str:
    try:
        content = fetch_article(url)
        return summarize(content)
    except Exception as exc:
        return f"**Error:** {exc}"


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Website Summarizer") as demo:
        gr.Markdown("# Website Summarizer\nPaste a URL to get a 3-5 bullet Markdown summary.")
        url = gr.Textbox(label="Website URL", placeholder="https://example.com")
        button = gr.Button("Summarize")
        summary = gr.Markdown(label="Summary")
        button.click(fn=run, inputs=url, outputs=summary)
        url.submit(fn=run, inputs=url, outputs=summary)
    return demo


if __name__ == "__main__":
    build_ui().launch()
