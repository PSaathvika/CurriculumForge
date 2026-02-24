import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"

def clean_ai_json(response_text):
    # Remove markdown code blocks
    response_text = re.sub(r"```json|```", "", response_text)

    # Remove JS-style comments
    response_text = re.sub(r"//.*", "", response_text)

    # Remove trailing commas before } or ]
    response_text = re.sub(r",\s*([\]}])", r"\1", response_text)

    # Extract JSON object safely
    match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if match:
        return match.group().strip()

    return response_text.strip()


def generate_curriculum(data):

    structured_prompt = """
    You are an academic curriculum designer.

    Generate a structured B.Tech curriculum in JSON format ONLY.

    IMPORTANT:
    - Return ONLY valid JSON.
    - Do NOT include explanations.
    - Do NOT include markdown.
    - Do NOT include extra text.
    - Follow the exact structure below.

    JSON Structure Required:

    {
    "curriculum": {
        "domain": "<skill domain>",
        "level": "<education level>",
        "industryOrientation": "<industry focus>",
        "semesters": <number>,
        "weeklyHours": <number>,
        "courses": [
        {
            "semester": 1,
            "courses": [
            {
                "name": "<course name>",
                "type": "theory/practical/lab",
                "hoursPerWeek": <number>,
                "description": ""
            }
            ]
        }
        ]
    }
    }

    Guidelines:
    - Distribute courses evenly across semesters.
    - Ensure weekly hours per semester do not exceed the provided weeklyHours.
    - Include 4–6 courses per semester.
    - Mix theory, practical, and lab courses.
    - Keep descriptions empty ("").
    - Ensure JSON is syntactically valid.

    Inputs:
    Skill Domain: {{skill}}
    Education Level: {{level}}
    Total Semesters: {{semesters}}
    Weekly Hours: {{hours}}
    Industry Focus: {{focus}}
    """
    print("Method Invoked")

    payload = {
        "model": "mistral",   # change to granite3.2:2b if needed
        "prompt": structured_prompt,
        "stream": False,
        "format": "json"      # Primary JSON enforcement
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code != 200:
            return {"error": "Ollama API error"}

        result = response.json()
        raw_output = result.get("response", "")
        
        print("RAW MODEL OUTPUT:\n", raw_output)

        # ✅ First Attempt: Direct JSON load (since format=json)
        try:
            return json.loads(raw_output)

        # ✅ Fallback: Clean + Retry
        except json.JSONDecodeError:
            print("Direct parse failed. Attempting clean fallback...")

            cleaned_text = clean_ai_json(raw_output)
            return json.loads(cleaned_text)

    except Exception as e:
        print("Final JSON Parsing Error:", str(e))
        return {"error": "Invalid JSON structure from model"}