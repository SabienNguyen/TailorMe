from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from matcher import match_resume_to_job

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/match", response_class=HTMLResponse)
async def match_resume(request: Request, resume: str = Form(...), job: str = Form(...)):
    score, breakdown = match_resume_to_job(resume, job)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "score": score,
        "interpretation": breakdown["interpretation"],
        "feedback": breakdown["feedback"],
        "resume": resume,
        "job": job
    })
