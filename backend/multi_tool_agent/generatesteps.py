# generate_steps.py
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os, json

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_steps(task: str, values: str, student: str) -> list[str]:
    prompt = (
        f"Create a step-by-step plan to solve a problem relating to {task} using {values}. "
        f"Write it so a {student} can understand it. "
        "Return ONLY JSON with a top-level object: {\"steps\": string[]}, no extra text. "
        "Each string in the 'steps' array must start with its number label like "
        "\"Step 1.\", \"Step 2.\", etc."
    )

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {"steps": {"type": "array", "items": {"type": "string"}}},
                "required": ["steps"],
            },
        ),
    )

    data = json.loads(resp.text)
    return data["steps"]  # <- this is just the array of strings


result = generate_steps("algebra", "basic algebraic operations", "high school student")  #Example usage
print(len(result))
for i in result:
    print(i)
