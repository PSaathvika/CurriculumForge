# openai_curriculum_function.py

import os
from typing import Dict
from openai import OpenAI
import json

# -----------------------------
# Initialize OpenAI client
# -----------------------------
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_KEY:
    raise ValueError("Missing OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_KEY)

# -----------------------------
# Default values
# -----------------------------
DEFAULTS = {
    "domain": "General",
    "level": "B.Tech",
    "industryOrientation": "General",
    "semesters": 8,
    "weeklyHours": 30,
    "courses": [],
}

# -----------------------------
# Curriculum JSON schema
# -----------------------------
def build_curriculum_schema():

    return {
        "type": "json_schema",
        "name": "curriculum",
        "schema": {
            "type": "object",
            "properties": {
                "curriculum": {
                    "type": "object",
                    "properties": {
                        "domain": {"type": "string"},
                        "level": {"type": "string"},
                        "industryOrientation": {"type": "string"},
                        "semesters": {"type": "integer"},
                        "weeklyHours": {"type": "integer"},
                        "courses": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "semester": {"type": "integer"},
                                    "courses": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"},
                                                "type": {
                                                    "type": "string",
                                                    "enum": ["theory", "practical", "lab"]
                                                },
                                                "hoursPerWeek": {"type": "integer"},
                                                "description": {"type": "string"}
                                            },
                                            "required": [
                                                "name",
                                                "type",
                                                "hoursPerWeek",
                                                "description"
                                            ],
                                            "additionalProperties": False
                                        }
                                    }
                                },
                                "required": ["semester", "courses"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": [
                        "domain",
                        "level",
                        "industryOrientation",
                        "semesters",
                        "weeklyHours",
                        "courses"
                    ],
                    "additionalProperties": False
                }
            },
            "required": ["curriculum"],
            "additionalProperties": False
        },
        "strict": True
    }

    return {
        "type": "json_schema",
        "name": "curriculum",
        "schema": {
            "type": "object",
            "properties": {
                "curriculum": {
                    "type": "object",
                    "properties": {
                        "domain": {"type": "string"},
                        "level": {"type": "string"},
                        "industryOrientation": {"type": "string"},
                        "semesters": {"type": "integer"},
                        "weeklyHours": {"type": "integer"},
                        "courses": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "semester": {"type": "integer"},
                                    "courses": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"},
                                                "type": {
                                                    "type": "string",
                                                    "enum": ["theory", "practical", "lab"]
                                                },
                                                "hoursPerWeek": {"type": "integer"},
                                                "description": {"type": "string"}
                                            },
                                            "required": [
                                                "name",
                                                "type",
                                                "hoursPerWeek",
                                                "description"
                                            ]
                                        }
                                    }
                                },
                                "required": ["semester", "courses"]
                            }
                        }
                    },
                    "required": [
                        "domain",
                        "level",
                        "industryOrientation",
                        "semesters",
                        "weeklyHours",
                        "courses"
                    ]
                }
            },
            "required": ["curriculum"],
            "additionalProperties": False
        },
        "strict": True
    }

# -----------------------------
# Apply fallback defaults
# -----------------------------
def apply_fallback(curriculum: Dict) -> Dict:

    if "curriculum" not in curriculum:
        curriculum["curriculum"] = {}

    for key, default in DEFAULTS.items():
        if key not in curriculum["curriculum"]:
            curriculum["curriculum"][key] = default

    for sem in curriculum["curriculum"]["courses"]:
        sem.setdefault("semester", 1)
        sem.setdefault("courses", [])

        for course in sem["courses"]:
            course.setdefault("name", "Unnamed Course")
            course.setdefault("type", "theory")
            course.setdefault("hoursPerWeek", 0)
            course.setdefault("description", "")

    return curriculum


# -----------------------------
# Generate curriculum
# -----------------------------
def generate_curriculum(data: Dict) -> Dict:

    domain = data.get("skill", DEFAULTS["domain"])
    level = data.get("level", DEFAULTS["level"])
    semesters = int(data.get("semesters", DEFAULTS["semesters"]))
    weekly_hours = int(data.get("hours", DEFAULTS["weeklyHours"]))
    focus = data.get("focus", DEFAULTS["industryOrientation"])

    system_prompt = "You are an expert academic curriculum designer."

    user_prompt = f"""
Generate a complete B.Tech curriculum.

Skill Domain: {domain}
Level: {level}
Semesters: {semesters}
Weekly Hours: {weekly_hours}
Industry Focus: {focus}

Distribute courses logically across semesters.
Include theory, practical and lab subjects.
Return only valid JSON.
"""

    try:

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            text={"format": build_curriculum_schema()},
            temperature=0.2
        )

        curriculum_json = json.loads(response.output_text)

        return apply_fallback(curriculum_json)

    except Exception as e:

        print("OpenAI API Error:", e)

        return apply_fallback({"curriculum": {}})