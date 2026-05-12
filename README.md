# Agentic Resume Screening

A lightweight resume screening app with a FastAPI backend and a Streamlit UI. Upload a PDF resume and get a structured evaluation against a fixed job description.

## Features

- PDF resume upload and parsing
- Job description extraction from a local PDF
- AI-based candidate evaluation
- Modern Streamlit UI

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- Streamlit
- OpenAI API

## Project Structure

```
agentic-resume-screening/
  app/
    main.py
    parsepdf.py
    prompts.py
    resume_screener.py
    agents/
      candidate_evaluation_agent.py
      jd_extractor_agent.py
      resume_extractor_agent.py
  resources/
    job_description.pdf
  ui/
    app.py
  requirements.txt
```

## Prerequisites

- Python 3.11+ installed
- OpenAI API key with available quota

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
pip install uvicorn
```

3. Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_key_here
```

## Run the Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

API runs at:

```
http://127.0.0.1:8000
```

## Run the UI

In a second terminal, from the project root:

```bash
cd ui
streamlit run app.py
```

## Usage

1. Open the Streamlit UI.
2. Upload a resume PDF.
3. Click **Process Resume** to view the evaluation.

## API Endpoint

- `POST /screening/`
  - Multipart form-data with key `resume`
  - Returns JSON with:
    - `candidate_status`
    - `reason`
    - `skill_match_percentage`

## Troubleshooting

- **Model not found**: Update the model name in the agent files.
- **Insufficient quota (429)**: Ensure the API key has available quota/billing.
- **JSON parse error**: The backend now handles error dicts; ensure you are on the latest code.

## Notes

- The job description is loaded from `resources/job_description.pdf`.
- The current model in use is `gpt-4o-mini`.
