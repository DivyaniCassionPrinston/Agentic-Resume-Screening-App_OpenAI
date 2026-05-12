import streamlit as st
import requests

st.set_page_config(
    page_title="Resume Screening",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    :root {
        --bg-1: #0f1115;
        --bg-2: #171a21;
        --panel: rgba(26, 30, 38, 0.75);
        --panel-border: rgba(255, 255, 255, 0.08);
        --accent: #35d0ba;
        --accent-2: #f3b85b;
        --text: #eef2f7;
        --muted: #a6b0c3;
    }

    html, body, [class*="css"]  {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background: radial-gradient(1200px 400px at 10% 10%, rgba(53, 208, 186, 0.15), transparent 60%),
                    radial-gradient(800px 500px at 90% 20%, rgba(243, 184, 91, 0.12), transparent 60%),
                    linear-gradient(180deg, var(--bg-1), var(--bg-2));
        color: var(--text);
    }

    .hero {
        padding: 2.5rem 2.25rem 2rem;
        border: 1px solid var(--panel-border);
        border-radius: 18px;
        background: var(--panel);
        backdrop-filter: blur(12px);
        animation: floatIn 0.7s ease-out;
    }

    .hero h1 {
        font-size: clamp(2rem, 4vw, 3.2rem);
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .hero p {
        color: var(--muted);
        font-size: 1.05rem;
        margin: 0.3rem 0 0;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        color: var(--accent);
        border: 1px solid rgba(53, 208, 186, 0.35);
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: rgba(53, 208, 186, 0.08);
    }

    .card {
        padding: 1.25rem 1.4rem;
        border: 1px solid var(--panel-border);
        border-radius: 16px;
        background: rgba(17, 20, 26, 0.75);
        min-height: 140px;
        animation: floatIn 0.9s ease-out;
    }

    .card h3 {
        margin-top: 0;
        margin-bottom: 0.4rem;
        font-size: 1.1rem;
    }

    .metric {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--accent-2);
        margin: 0.2rem 0;
    }

    .stButton > button {
        background: linear-gradient(135deg, #35d0ba, #f3b85b);
        color: #0b0d12;
        border: none;
        border-radius: 999px;
        padding: 0.6rem 1.3rem;
        font-weight: 600;
        transition: transform 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
    }

    .stFileUploader > label {
        font-weight: 600;
    }

    .result-box {
        border: 1px solid rgba(53, 208, 186, 0.25);
        background: rgba(8, 12, 18, 0.6);
        padding: 1.2rem 1.4rem;
        border-radius: 14px;
        margin-top: 1rem;
    }

    .result-label {
        font-size: 0.9rem;
        color: var(--muted);
        margin-bottom: 0.15rem;
    }

    @keyframes floatIn {
        0% { opacity: 0; transform: translateY(8px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 900px) {
        .hero { padding: 2rem 1.5rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="pill">AI Resume Screening</div>
        <h1>Resume Screening App</h1>
        <p>Upload a resume, match it against a fixed job description, and get an instant, structured evaluation.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

left, right = st.columns([1.2, 1])

with left:
    st.subheader("Upload")
    uploaded_file = st.file_uploader("Upload a resume (PDF)", type="pdf")
    st.caption("We only accept PDF resumes. Your file is processed locally and sent to the API for evaluation.")

    if uploaded_file is not None:
        st.success(f"File uploaded successfully: {uploaded_file.name}")
        print("File uploaded successfully:", uploaded_file.name)

    process_clicked = st.button("Process Resume", use_container_width=True)

with right:
    st.markdown(
        """
        <div class="card">
            <h3>What you get</h3>
            <p>Clear candidate status, skill match percentage, and actionable feedback.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        """
        <div class="card">
            <h3>Pipeline</h3>
            <p>PDF parsing → Resume extraction → JD extraction → Final evaluation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if uploaded_file is not None and process_clicked:
    with st.spinner("Analyzing resume and matching against the job description..."):
        response = requests.post(
            "http://localhost:8000/screening/",
            files={"resume": uploaded_file},
            timeout=120,
        )

    if response.status_code == 200:
        response_data = response.json()
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.markdown("<div class='result-label'>Candidate Status</div>", unsafe_allow_html=True)
        st.subheader(response_data.get("candidate_status", "Unknown"))
        st.markdown("<div class='result-label'>Skills Matched</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='metric'>{response_data.get('skill_match_percentage', 0)}%</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div class='result-label'>Feedback</div>", unsafe_allow_html=True)
        st.write(response_data.get("reason", "No feedback provided."))
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Error processing resume. See details below.")
        st.code(response.text, language="json")


