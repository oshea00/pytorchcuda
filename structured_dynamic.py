import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
from pydantic import BaseModel, Field, create_model

from typing import Any, Dict, List
import json
import difflib


class Message(BaseModel):
    role: str
    content: str


class CalendarEvent(BaseModel):
    event_name: str = Field(
        ..., description="The name of the event"
    )
    start_date: str = Field(
        ..., description="The start date of the event"
    )
    participants: List[str] = Field(
        ...,
        description="The participants of the event",
    )


calendar_event_schema = (
    CalendarEvent.model_json_schema()
)
calendar_event_schema_json = json.dumps(
    calendar_event_schema, indent=2
)
print(calendar_event_schema_json)


def create_received_schema_dict_json(
    schema: Dict[str, Any]
) -> Dict[str, Any]:
    received_dict = {
        "type": "json_schema",
        "json_schema": schema,
        "name": schema["title"],
        "strict": True,
    }
    return json.dumps(received_dict, indent=2)


def create_received_schema_dict(
    schema: Dict[str, Any]
) -> Dict[str, Any]:
    received_dict = {
        "type": "json_schema",
        "json_schema": schema,
        "name": schema["title"],
        "strict": True,
    }
    return received_dict


# Example JSON schema you received
received_schema = create_received_schema_dict(
    calendar_event_schema
)

print(received_schema)


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
            item_type = field_props["items"]["type"]
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
            field_info = (python_type, ...)
        else:
            field_info = (python_type, None)

        # Include description if present
        if "description" in field_props:
            field_info = Field(
                default=field_info[1],
                description=field_props["description"],
            )

        fields[field_name] = field_info

    # Dynamically create the Pydantic model
    return create_model(schema["title"], **fields)


# Generate Pydantic model from schema
dynamic_model = json_schema_to_pydantic_model(
    received_schema["json_schema"]
)

# Print generated model schema (optional)
dynamic_model_schema = json.dumps(
    dynamic_model.model_json_schema(), indent=2
)
print(dynamic_model_schema)


def generate_schema_diff(
    schema1: str, schema2: str
) -> str:
    diff = difflib.unified_diff(
        schema1.splitlines(),
        schema2.splitlines(),
        lineterm="",
    )
    return "\n".join(diff)


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


if calendar_event_schema_json == dynamic_model_schema:
    print("The schemas are not equal")
    schema_diff = generate_schema_diff(
        calendar_event_schema_json,
        dynamic_model_schema,
    )
    print("Schema differences:\n", schema_diff)
