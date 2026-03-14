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