from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from app.parsepdf import parse_pdf
from app.agents.resume_extractor_agent import analyze_resume
from app.agents.jd_extractor_agent import analyze_jd
from app.agents.candidate_evaluation_agent import evaluate_candidate
import json

app = FastAPI()

@app.post("/screening/")
async def upload_resume(resume: UploadFile):
    """
    Endpoint to upload a resume file.
    """
    print("Received resume file:", resume.filename)

    resume_text = parse_pdf(resume.file)

    candidate_details = analyze_resume(resume_text)

    jd_text = ""
    with open ("resources/job_description.pdf", "rb") as file:
        jd_text = parse_pdf(file)

    jd_details = analyze_jd(jd_text)

    evaluation = evaluate_candidate(candidate_details, jd_details)

    print("Evaluation result:", evaluation)

    if isinstance(evaluation, dict):
        return JSONResponse(content=evaluation, status_code=502)

    result_json = json.loads(evaluation)
    return JSONResponse(content=result_json)
    
    