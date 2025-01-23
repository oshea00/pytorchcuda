import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
from pydantic import (
    BaseModel,
    Field,
    create_model,
)
from typing import Any, Dict, List
import json


class Message(BaseModel):
    role: str
    content: str


class CalendarEvent(BaseModel):
    event_name: str
    start_date: str
    participants: List[str]


payload_list_format = (
    CalendarEvent.model_json_schema()
)
print(f"payload_schema: {payload_list_format}")

payload_response_format_list = {
    "type": "json_schema",
    "json_schema": {
        "schema": {
            "properties": {
                "event_name": {
                    "title": "Event Name",
                    "type": "string",
                },
                "start_date": {
                    "title": "Start Date",
                    "type": "string",
                },
                "participants": {
                    "items": {"type": "string"},
                    "title": "Participants",
                    "type": "array",
                },
            },
            "required": [
                "event_name",
                "start_date",
                "participants",
            ],
            "title": "CalendarEvent",
            "type": "object",
        }
    },
    "name": "CalendarEvent",
    "strict": True,
}

payload_response_format = {
    "type": "json_schema",
    "json_schema": {
        "schema": {
            "properties": {
                "event_name": {
                    "title": "event_name",
                    "type": "string",
                },
                "start_date": {
                    "title": "start_date",
                    "type": "string",
                },
            },
            "required": [
                "event_name",
                "start_date",
            ],
            "title": "CalendarEvent",
            "type": "object",
        }
    },
    "name": "CalendarEvent",
    "strict": True,
}

# Example JSON schema you received
received_schema = payload_response_format_list[
    "json_schema"
]["schema"]


# Function to convert JSON schema to a Pydantic model
def json_schema_to_pydantic_model(
    schema: Dict[str, Any]
) -> Any:
    fields = {}

    for field_name, field_props in schema.get(
        "properties", {}
    ).items():
        field_type = field_props["type"]

        # Mapping JSON schema types to Python types
        type_mapping = {
            "string": str,
            "integer": int,
            "boolean": bool,
            "number": float,
            "array": list,
            "object": dict,
        }

        if field_type == "array":
            item_type = field_props["items"][
                "type"
            ]
            python_type = List[
                type_mapping.get(item_type, Any)
            ]
        else:
            python_type = type_mapping.get(
                field_type, Any
            )

        # Required fields handling
        if (
            "required" in schema
            and field_name in schema["required"]
        ):
            fields[field_name] = (
                python_type,
                ...,
            )
        else:
            fields[field_name] = (
                python_type,
                None,
            )

    # Dynamically create the Pydantic model
    return create_model(
        payload_response_format["name"], **fields
    )


# Generate Pydantic model from schema
dynamic_model = json_schema_to_pydantic_model(
    received_schema
)

# Print generated model schema (optional)
print(
    f"dynamic_schema: {dynamic_model.model_json_schema()}"
)

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        Message(
            role="user",
            content="Mike is going to dinner on his birthday 2/3",
        )
    ],
    response_format=dynamic_model,
)

print(response.choices[0].message.parsed)
