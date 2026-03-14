import json
import re
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def improve_bullet_point(bullet_point):

    prompt = f"""
You are an expert resume writer.

Rewrite the following weak resume bullet point into a strong,
professional bullet point with measurable achievements.

Weak Bullet Point:
{bullet_point}

Return ONLY valid JSON in this format:

{{
 "improved_bullet_point": "..."
}}

Rules:
- Start with a strong action verb
- Add measurable impact if possible
- Make it concise and professional
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        content = response.choices[0].message.content

        # clean markdown
        content = re.sub(r"```json|```", "", content).strip()

        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            return json.loads(match.group(0))

        return {"error": "Invalid AI response"}

    except Exception as e:
        return {"error": str(e)}