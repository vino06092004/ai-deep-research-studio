# 🔷 AI Deep Research Studio

A visually polished AI research application built with Python, Streamlit, Tavily Search API, and Google Gemini.

## Features
- Live web search using Tavily
- Structured AI-generated research reports using Gemini
- Source/evidence tab with clickable original URLs
- Interactive follow-up chat grounded in the generated report
- Markdown and plain-text report downloads
- Responsive dark navy, blue, and cyan interface

## Project files
```text
ai_deep_research_studio/
├── app.py
├── research.py
├── requirements.txt
└── .streamlit/
    └── secrets.toml
```

Keep your existing `research.py`: this interface imports `search_tavily`, `generate_report`, and `answer_research_chat` from it.

## 1. Install dependencies
Open a terminal in the project folder:
```bash
python -m venv .venv
```
Windows:
```bash
.venv\Scripts\activate
```
Install packages:
```bash
pip install -r requirements.txt
```

## 2. Configure API keys
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "paste_your_gemini_api_key_here"
TAVILY_API_KEY = "paste_your_tavily_api_key_here"
```
Never commit `secrets.toml` or share API keys publicly. Add `.streamlit/secrets.toml` to `.gitignore`.

## 3. Run
```bash
streamlit run app.py
```

## Notes
- This replacement updates the Streamlit UI in `app.py`. It assumes your existing `research.py` provides the three imported functions with compatible arguments.
- If your current `research.py` uses different function names or parameter names, adapt the imports/calls to match it.
- Search results and AI summaries can be incomplete or inaccurate. Open the original sources to verify important claims.
