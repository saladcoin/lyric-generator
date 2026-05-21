from openai import OpenAI
from app.config import LLM_API_KEY, LLM_API_BASE, LLM_MODEL

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_API_BASE)
    return _client


def chat_completion(messages: list, temperature: float = 0.8) -> str:
    client = get_client()
    resp = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=3072,
    )
    return resp.choices[0].message.content
