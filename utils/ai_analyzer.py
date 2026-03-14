import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv(".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text):

    resume_text = resume_text[:4000]

    prompt = f"""
Evaluate the following resume for ATS compatibility.

Resume:
{resume_text}

Return ONLY valid JSON.

Format:

{{
 "ATS_score": number,
 "keyword_match_score": number,
 "formatting_score": number,
 "experience_score": number,
 "skills_score": number,
 "strengths": [],
 "weaknesses": [],
 "missing_keywords": [],
 "improvement_suggestions": []
}}

All scores must be between 0 and 100.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content

    content = re.sub(r"```json|```", "", content).strip()

    match = re.search(r"\{.*\}", content, re.DOTALL)

    if match:
        return json.loads(match.group(0))

    return {"error": "AI returned invalid JSON"}



def match_job_role(resume_text, job_role):

    resume_text = resume_text[:4000]

    prompt = f"""
You are an AI recruitment assistant.

Compare the following resume with the target job role.

Resume:
{resume_text}

Target Job Role:
{job_role}

Return ONLY valid JSON in this format:

{{
 "job_match_score": number,
 "matching_skills": [],
 "missing_skills": [],
 "recommendations": []
}}

Rules:
- job_match_score must be between 0 and 100.
- matching_skills → skills present in resume relevant to the job role.
- missing_skills → skills required for the role but missing in resume.
- recommendations → suggestions to improve the resume for this job role.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content

        import re, json
        content = re.sub(r"```json|```", "", content).strip()
        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            return json.loads(match.group(0))

        return {"error": "Invalid AI response"}

    except Exception as e:
        return {"error": str(e)}