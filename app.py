import streamlit as st
from research import search_tavily, generate_report, answer_research_chat

st.set_page_config(
    page_title="AI Deep Research Studio",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------- VISUAL DESIGN ---------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #07111f;
  --panel: #0d1b2d;
  --panel2: #10243a;
  --line: rgba(148, 190, 225, .16);
  --text: #edf6ff;
  --muted: #9db2c9;
  --cyan: #38d9ff;
  --blue: #5794ff;
  --purple: #9b8cff;
}
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
  background:
    radial-gradient(ellipse at 12% 0%, rgba(42, 110, 220, .19), transparent 34%),
    radial-gradient(ellipse at 88% 12%, rgba(34, 211, 238, .10), transparent 28%),
    #07111f;
  color: var(--text);
}
[data-testid="stHeader"] { background: rgba(7,17,31,.7); }
.block-container { max-width: 1440px; padding-top: 2rem; padding-bottom: 4rem; }
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0b1728 0%, #091321 100%);
  border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }
h1, h2, h3 { font-family: 'Manrope', sans-serif; letter-spacing: -.035em; }
h1 { color: #f5fbff; }
p, li, label { color: #d7e6f4; }
small, [data-testid="stCaptionContainer"] { color: var(--muted) !important; }
.hero {
  position: relative; overflow: hidden;
  padding: 2.4rem 2.5rem; border-radius: 26px;
  background: linear-gradient(120deg, rgba(20,42,78,.97), rgba(12,80,126,.92) 58%, rgba(16,147,174,.85));
  border: 1px solid rgba(108,211,255,.3);
  box-shadow: 0 18px 60px rgba(0,0,0,.22);
  margin-bottom: 1.6rem;
}
.hero:after {
  content: ""; position:absolute; width:290px; height:290px; right:-70px; top:-130px;
  border:1px solid rgba(255,255,255,.14); border-radius:50%;
  box-shadow:0 0 0 35px rgba(255,255,255,.025),0 0 0 70px rgba(255,255,255,.02);
}
.eyebrow {
  display:inline-block; padding:6px 11px; border-radius:999px;
  background:rgba(56,217,255,.12); border:1px solid rgba(56,217,255,.28);
  color:#9ceeff; font-size:.76rem; font-weight:700; letter-spacing:.11em; text-transform:uppercase;
}
.hero h1 { font-size:clamp(2rem,4vw,3.15rem); line-height:1.12; margin:.9rem 0 .65rem; color:white; }
.hero p { max-width:780px; color:#d7f0ff; font-size:1.02rem; line-height:1.7; margin:0; }
.section-label { color:#7ce9ff; font-size:.76rem; font-weight:800; letter-spacing:.13em; text-transform:uppercase; margin:.3rem 0 .45rem; }
.panel {
  background:linear-gradient(145deg, rgba(17,36,58,.96), rgba(10,25,42,.96));
  border:1px solid var(--line); border-radius:20px; padding:1.25rem 1.35rem;
}
.metric-card {
  min-height:115px; padding:1rem 1.1rem; border-radius:18px;
  background:linear-gradient(145deg, rgba(17,39,64,.98), rgba(10,26,44,.98));
  border:1px solid var(--line);
}
.metric-label { color:#9db7d1; font-size:.82rem; margin-bottom:.55rem; }
.metric-value { color:#f4fbff; font-family:'Manrope',sans-serif; font-size:1.75rem; font-weight:800; }
.metric-note { color:#6ee7f9; font-size:.75rem; margin-top:.25rem; }
div.stButton > button, div[data-testid="stDownloadButton"] > button {
  border:1px solid rgba(95,205,255,.35); border-radius:12px; min-height:2.7rem;
  font-weight:700; transition:all .2s ease;
}
div.stButton > button[kind="primary"] {
  color:#061421; background:linear-gradient(100deg,#70e7ff,#60a5fa 58%,#a5a0ff);
  border:0; box-shadow:0 7px 24px rgba(56,189,248,.18);
}
div.stButton > button:hover, div[data-testid="stDownloadButton"] > button:hover {
  transform:translateY(-1px); border-color:#6ce8ff;
}
div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, textarea {
  background:#0a1929 !important; border-color:rgba(148,190,225,.22) !important; border-radius:12px !important;
}
.stTabs [data-baseweb="tab-list"] { gap:8px; border-bottom:1px solid var(--line); }
.stTabs [data-baseweb="tab"] {
  background:rgba(15,35,57,.72); border:1px solid transparent; border-radius:11px 11px 0 0;
  padding:10px 16px; color:#a8bdd1; font-weight:700;
}
.stTabs [aria-selected="true"] {
  background:rgba(56,217,255,.10) !important; border-color:rgba(56,217,255,.25) !important;
  color:#82eaff !important;
}
div[data-testid="stExpander"] { border:1px solid var(--line); border-radius:13px; background:rgba(13,30,49,.7); }
div[data-testid="stChatMessage"] { background:rgba(13,30,49,.75); border:1px solid var(--line); border-radius:15px; }
hr { border-color:var(--line); }
.footer { color:#7891aa; font-size:.78rem; text-align:center; padding:1.5rem 0 .2rem; }
a { color:#79e7ff !important; }
</style>
""", unsafe_allow_html=True)

# --------------------------- STATE ---------------------------
defaults = {"report": None, "sources": [], "query": "", "chat_messages": [], "report_tone": "Beginner-Friendly"}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------- SIDEBAR ---------------------------
with st.sidebar:
    st.markdown("## 🔷 Research Studio")
    st.caption("Your AI-powered research workspace")
    st.markdown("---")
    max_sources = st.slider("Sources to retrieve", 3, 8, 5, help="Number of web results to include in the research context.")
    search_depth = st.radio("Search depth", ["basic", "advanced"], index=0, help="Advanced search can take longer.")
    report_tone = st.selectbox("Report style", ["Beginner-Friendly", "Academic / Formal", "Executive Summary"], index=0)
    st.markdown("---")
    st.markdown("**Workflow**")
    st.markdown("`01`  Search the web\n\n`02`  Synthesize a report\n\n`03`  Explore sources\n\n`04`  Ask follow-up questions")
    st.markdown("---")
    if st.button("↻ Start a new research session", use_container_width=True):
        for key in ["report", "sources", "query", "chat_messages"]:
            st.session_state[key] = defaults[key]
        st.rerun()
    st.caption("Powered by Tavily Search + Google Gemini")

# --------------------------- HERO ---------------------------
st.markdown("""
<div class="hero">
  <span class="eyebrow">AI-powered knowledge workspace</span>
  <h1>Research deeper.<br>Understand faster.</h1>
  <p>Turn a topic into a structured, source-grounded research report. Explore the evidence, download your findings, and ask follow-up questions in one workspace.</p>
</div>
""", unsafe_allow_html=True)

# --------------------------- API CONFIG ---------------------------
try:
    gemini_key = st.secrets.get("GEMINI_API_KEY", "").strip()
    tavily_key = st.secrets.get("TAVILY_API_KEY", "").strip()
except Exception:
    gemini_key, tavily_key = "", ""

if not gemini_key or not tavily_key:
    st.error("API keys are missing. Add GEMINI_API_KEY and TAVILY_API_KEY to `.streamlit/secrets.toml`.")
    with st.expander("How to configure your API keys"):
        st.code('GEMINI_API_KEY = "your_gemini_api_key"\nTAVILY_API_KEY = "your_tavily_api_key"', language="toml")
    st.stop()

# --------------------------- SEARCH INPUT ---------------------------
st.markdown('<div class="section-label">Start your investigation</div>', unsafe_allow_html=True)
with st.form("research_form", clear_on_submit=False):
    user_query = st.text_input(
        "Research topic",
        value=st.session_state.get("query", ""),
        placeholder="e.g., How are AI agents changing healthcare?",
        help="Be specific for more focused research.",
    )
    submit_col, hint_col = st.columns([1, 3], vertical_alignment="center")
    with submit_col:
        run_btn = st.form_submit_button("✦ Conduct research", type="primary", use_container_width=True)
    with hint_col:
        st.caption("Tip: include a technology, industry, timeframe, or question for more useful findings.")

if run_btn:
    if not user_query.strip():
        st.warning("Enter a research topic before starting.")
    else:
        st.session_state["query"] = user_query.strip()
        st.session_state["chat_messages"] = []
        st.session_state["report"] = None
        st.session_state["sources"] = []
        try:
            with st.status("Running your research pipeline…", expanded=True) as status:
                st.write("🔎 **Step 1 of 2 — Tavily** is retrieving relevant web context.")
                context, sources, _ = search_tavily(
                    query=user_query.strip(),
                    api_key=tavily_key,
                    max_results=max_sources,
                    search_depth=search_depth,
                )
                if not sources:
                    status.update(label="No sources found", state="error", expanded=True)
                    st.warning("No relevant sources were returned. Try a broader or more specific query.")
                    st.stop()
                st.write(f"🧠 **Step 2 of 2 — Gemini** is synthesizing findings from {len(sources)} source(s).")
                report = generate_report(
                    query=user_query.strip(),
                    context=context,
                    gemini_api_key=gemini_key,
                    tone=report_tone,
                )
                st.session_state["report"] = report
                st.session_state["sources"] = sources
                st.session_state["report_tone"] = report_tone
                status.update(label="Research complete", state="complete", expanded=False)
        except Exception as exc:
            st.error(f"Research failed: {exc}")
            st.info("Check your API keys, internet connection, and the functions in `research.py`.")

# --------------------------- RESULTS ---------------------------
if st.session_state["report"]:
    sources = st.session_state["sources"]
    report = st.session_state["report"]
    st.markdown("")
    st.markdown('<div class="section-label">Research workspace</div>', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Research topic</div><div class="metric-value" style="font-size:1.05rem">{st.session_state["query"][:46]}{"…" if len(st.session_state["query"]) > 46 else ""}</div><div class="metric-note">Your active investigation</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Sources retrieved</div><div class="metric-value">{len(sources)}</div><div class="metric-note">Web evidence to explore</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Report style</div><div class="metric-value" style="font-size:1.15rem">{st.session_state.get("report_tone", report_tone)}</div><div class="metric-note">Selected writing style</div></div>', unsafe_allow_html=True)

    st.markdown("")
    tab_report, tab_sources, tab_chat = st.tabs(["📑  Research report", "🌐  Sources & evidence", "💬  Ask the report"])

    with tab_report:
        left, right = st.columns([1, 1])
        with left:
            st.caption("Your generated report")
        with right:
            st.caption("Download a copy for your portfolio or notes")
        dl1, dl2, _ = st.columns([1, 1, 3])
        with dl1:
            st.download_button("↓ Markdown", data=report, file_name="ai_research_report.md", mime="text/markdown", use_container_width=True)
        with dl2:
            st.download_button("↓ Plain text", data=report, file_name="ai_research_report.txt", mime="text/plain", use_container_width=True)
        st.markdown("---")
        st.markdown(report)

    with tab_sources:
        st.markdown("### Evidence library")
        st.caption("Open the original pages to verify details and read beyond the search snippets.")
        if not sources:
            st.info("No source list was saved for this report.")
        for src in sources:
            title = src.get("title", "Untitled source")
            url = src.get("url", "")
            snippet = src.get("snippet", "No preview available.")
            index = src.get("index", "")
            with st.expander(f"🔗  {index}. {title}" if index != "" else f"🔗  {title}"):
                if url:
                    st.markdown(f"**Source URL:** [{url}]({url})")
                st.write(snippet)

    with tab_chat:
        st.markdown("### Ask questions about your findings")
        st.caption("Answers are generated using the report as context. For claims that matter, check the source links.")
        for msg in st.session_state["chat_messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        prompt = st.chat_input("Ask for a summary, comparison, explanation, or key takeaway…")
        if prompt:
            st.session_state["chat_messages"].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Reading the report and preparing an answer…"):
                    try:
                        reply = answer_research_chat(
                            user_question=prompt,
                            report_context=report,
                            gemini_api_key=gemini_key,
                        )
                        st.markdown(reply)
                        st.session_state["chat_messages"].append({"role": "assistant", "content": reply})
                    except Exception as exc:
                        st.error(f"Chat failed: {exc}")
                        st.caption("Check `answer_research_chat` in research.py and verify your Gemini API key.")

else:
    st.markdown("")
    st.markdown('<div class="section-label">Your workflow</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="panel"><div style="font-size:1.8rem">🔎</div><h3>01 · Discover</h3><p>Search the live web for relevant information and source previews.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel"><div style="font-size:1.8rem">🧠</div><h3>02 · Synthesize</h3><p>Use Gemini to organize retrieved context into a readable report.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="panel"><div style="font-size:1.8rem">💬</div><h3>03 · Explore</h3><p>Ask follow-up questions based on the generated report.</p></div>', unsafe_allow_html=True)
    st.markdown("")
    st.info("Your report and evidence tabs will appear here after you conduct your first research session.")

st.markdown('<div class="footer">AI Deep Research Studio · Built with Streamlit, Tavily and Google Gemini</div>', unsafe_allow_html=True)
