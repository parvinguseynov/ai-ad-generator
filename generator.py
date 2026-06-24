import os
import anthropic
from dotenv import load_dotenv
import json
from pydantic import BaseModel, ValidationError

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def generate_content(prompt: str) -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return message.content[0].text


def clean_json_response(raw: str) -> str:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
    if text.endswith("```"):
        text = text.rsplit("\n", 1)[0]
    return text.strip()


def parse_and_validate(raw: str, schema: type[BaseModel]) -> BaseModel | None:
    cleaned = clean_json_response(raw)
    try:
        data = json.loads(cleaned)
        return schema(**data)
    except (json.JSONDecodeError, ValidationError):
        return None
