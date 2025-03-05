from typing import Dict, Any, Optional
from pydantic import BaseModel
from openai import OpenAI
import json
from fastapi import FastAPI, HTTPException

client = OpenAI(base_url="http://localhost:8088/v1")


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


def handle_completion(payload: Dict[str, Any]) -> Dict[str, Any]:

    validation = validate_response_format(payload)

    try:
        if validation["has_response_format"]:
            if not validation["is_valid"]:
                raise HTTPException(status_code=400, detail=validation["error"])

            # Use parse endpoint with schema
            response = client.beta.chat.completions.parse(
                messages=payload.get("messages", []),
                model=payload.get("model", "gpt-4o"),
                response_format={
                    "type": "json_schema",
                    "json_schema": validation["json_schema"],
                },
            )
        else:
            # Regular completion without schema
            response = client.chat.completions.create(**payload)

        return response
    except Exception as e:
        print(e)


def validate_response_format(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the response_format in the incoming payload.

    Args:
        payload: The incoming request payload

    Returns:
        Dict containing validation results
    """
    # Check if response_format exists
    if "response_format" not in payload:
        return {"has_response_format": False}

    response_format = payload["response_format"]

    # Validate basic structure
    if (
        not isinstance(response_format, dict)
        or "type" not in response_format
        or "json_schema" not in response_format
    ):
        return {
            "has_response_format": True,
            "is_valid": False,
            "error": "Invalid response_format structure",
        }

    # Validate type is json_schema
    if response_format["type"] != "json_schema":
        return {
            "has_response_format": True,
            "is_valid": False,
            "error": 'response_format.type must be "json_schema"',
        }

    # Validate json_schema structure
    json_schema = response_format["json_schema"]
    if "schema" not in json_schema or not isinstance(json_schema["schema"], dict):
        return {
            "has_response_format": True,
            "is_valid": False,
            "error": "Invalid json_schema.schema structure",
        }

    # Return the validated schema
    return {
        "has_response_format": True,
        "is_valid": True,
        "json_schema": {
            "name": json_schema["name"],
            "strict": json_schema.get("strict", False),
            "schema": json_schema["schema"],
        },
    }


payload = {
    "messages": [
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    "model": "gpt-4o",
    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "schema": {
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "date": {"title": "Date", "type": "string"},
                    "participants": {
                        "items": {"type": "string"},
                        "title": "Participants",
                        "type": "array",
                    },
                },
                "required": ["name", "date", "participants"],
                "title": "CalendarEvent",
                "type": "object",
                "additionalProperties": False,
            },
            "name": "CalendarEvent",
            "strict": True,
        },
    },
    "stream": False,
}


event = handle_completion(payload)
print(json.dumps(event.choices[0].message.content, indent=2))
