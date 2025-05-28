# matcher.py
import openai
import numpy as np
from typing import Tuple
import os

# Load API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

def interpret_score(score: float) -> str:
    if score >= 0.9:
        return "Excellent match!"
    elif score >= 0.75:
        return "Strong match"
    elif score >= 0.6:
        return "Moderate match – could improve"
    else:
        return "Weak match – consider tailoring more"

def generate_gpt_feedback(resume_text: str, job_text: str) -> str:
    prompt = f"""
You are a career coach. Given the resume and job description below, give constructive feedback on how well the resume matches the job.

1. List 2–3 strengths in bullet points.
2. List 2–3 weaknesses or gaps in bullet points.
3. Suggest 2–3 specific improvements to tailor the resume to this job.

Resume:
{resume_text}

Job Description:
{job_text}
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful career coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def match_resume_to_job(resume_text: str, job_text: str) -> Tuple[float, dict]:
    resume_vec = get_embedding(resume_text)
    job_vec = get_embedding(job_text)
    score = cosine_similarity(resume_vec, job_vec)

    feedback = generate_gpt_feedback(resume_text, job_text)

    breakdown = {
        "raw_cosine_similarity": round(score, 4),
        "interpretation": interpret_score(score),
        "feedback": feedback
    }

    return round(score, 4), breakdown
