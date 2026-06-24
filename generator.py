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


def generate_for_platform(
    business: str,
    product: str,
    prompt_builder,
    schema: type[BaseModel],
    retries: int = 1,
) -> BaseModel | None:
    prompt = prompt_builder(business, product)
    for attempt in range(retries + 1):
        raw = generate_content(prompt)
        result = parse_and_validate(raw, schema)
        if result is not None:
            return result
    return None
