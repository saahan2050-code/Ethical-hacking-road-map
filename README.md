# 🛡️ Ethical Hacking Roadmap

A Streamlit app that gives learners a complete, step-by-step roadmap to becoming an ethical hacker, plus an AI mentor powered by **Google Gemini Flash**.

## Features

- 🗺️ **Complete roadmap** – 10 phases (ethics & law → networking → programming → web security → pentesting → CTFs → specialization → certifications), each with topics, tools, resources and a mini-project. Works without an API key.
- ✅ **Progress tracker** – tick topics off, see per-phase and overall progress, download a JSON report.
- 🎯 **AI personalised plan** – choose your level, goal, weekly hours and duration; Gemini builds a week-by-week plan (downloadable as Markdown).
- 💬 **AI mentor chat** – ask about concepts, tools, labs, certs and careers. The system prompt keeps answers legal and defensive-minded and refuses malicious requests.
- ⚖️ **Ethics & law** – the ethical hacker's code and a list of legal practice platforms.

## Project structure

```
.
├── app.py             # the whole app
├── requirements.txt   # Python dependencies
└── README.md
```

## Run locally

1. Install Python 3.10+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get a free Gemini API key at <https://aistudio.google.com/apikey>.
4. Provide the key in **one** of these ways:
   - Paste it in the app's sidebar (easiest), **or**
   - Set an environment variable:
     - macOS/Linux: `export GEMINI_API_KEY="your-key"`
     - Windows (PowerShell): `$env:GEMINI_API_KEY="your-key"`
   - **or** create `.streamlit/secrets.toml` containing:
     ```toml
     GEMINI_API_KEY = "your-key"
     ```
5. Start the app:
   ```bash
   streamlit run app.py
   ```

## Configuration

| Setting | Where | Default |
|---|---|---|
| Gemini API key | Sidebar / `GEMINI_API_KEY` secret / env var | – |
| Model name | Sidebar | `gemini-2.5-flash` |

If Google renames or retires a model, just type the new Flash model name into the sidebar – no code change needed.

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (public or private).
2. Go to <https://share.streamlit.io> and sign in with GitHub.
3. Click **Create app** → **Deploy a public app from GitHub**.
4. Choose your repository, branch `main`, and main file path `app.py`.
5. Open **Advanced settings → Secrets** and paste:
   ```toml
   GEMINI_API_KEY = "your-key"
   ```
6. Click **Deploy**.

> ⚠️ Never commit your API key to GitHub. Use Secrets.

## Disclaimer

This project is for **educational purposes only**. Only test systems you own or have explicit written permission to test. Unauthorized access to computer systems is illegal.

## License

MIT – use it, modify it, share it.
