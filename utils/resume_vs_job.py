import json
import re
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_resume_vs_job(resume_text, job_description):

    prompt = f"""
You are an AI recruitment assistant.

Compare the following resume with the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY valid JSON in this format:

{{
 "match_score": number,
 "matching_keywords": [],
 "missing_keywords": [],
 "recommendations": []
}}

Rules:
- match_score must be between 0 and 100
- matching_keywords → skills present in both resume and job description
- missing_keywords → skills required in job description but missing in resume
- recommendations → how candidate can improve resume for this role
"""

    try:

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

        return {"error": "Invalid AI response"}

    except Exception as e:
        return {"error": str(e)}