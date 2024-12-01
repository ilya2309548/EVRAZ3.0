import aiohttp
import os


async def send_to_llm(content):
    """Отправка данных в LLM API"""
    LLM_API_URL = os.getenv("LLM_API_URL")
    LLM_API_KEY = os.getenv("LLM_API_KEY")

    headers = {"Authorization": LLM_API_KEY, "Content-Type": "application/json"}
    payload = {
        "model": "mistral-nemo-instruct-2407",
        "messages": [
            {"role": "system", "content": "отвечай на русском языке"},
            {"role": "user", "content": content},
        ],
        "max_tokens": 1000,
        "temperature": 0.3,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            LLM_API_URL, headers=headers, json=payload
        ) as response:
            return await response.json()
