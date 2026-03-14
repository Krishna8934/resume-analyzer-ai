import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


def analyze_resume(resume_text):

    resume_text = resume_text[:4000]

    prompt = f"""
Analyze the following resume and give structured feedback.

Resume:
{resume_text}

Return ONLY valid JSON. Do not include explanations.

Format:

{{
  "ATS_score": number,
  "strengths": [],
  "weaknesses": [],
  "missing_keywords": [],
  "improvement_suggestions": []
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content

        # remove markdown if present
        content = re.sub(r"```json|```", "", content).strip()

        return json.loads(content)

    except Exception as e:
        return {"error": str(e)}