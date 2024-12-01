import requests
import os
from bot.utils import split_text
from datetime import datetime

# Получаем токен Hugging Face из переменных окружения
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"


def send_request_to_hf(prompt):
    """
    Отправляет запрос к Hugging Face API с указанным prompt.
    """
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": prompt}

    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"]
    else:
        raise Exception(
            f"Ошибка Hugging Face API: {response.status_code} - {response.text}"
        )


async def get_review(
    file_content, rules, initial_chunk_size=512, min_chunk_size=64
):
    """
    Отправляет содержимое файла и правила в Hugging Face API для анализа.
    """
    rules_text = "\n".join([f"- {rule['rule']}" for rule in rules])
    chunk_size = initial_chunk_size
    text_chunks = split_text(file_content, max_tokens=chunk_size)
    results = []

    for chunk in text_chunks:
        try:
            prompt = (
                f"На основе следующих правил:\n{rules_text}\n\n"
                f"Проанализируйте следующий текст:\n{chunk}\n\n"
                "Укажите ошибки и рекомендации."
            )
            result = send_request_to_hf(prompt)
            results.append(result)
        except Exception as e:
            results.append(f"Ошибка анализа текста: {e}")

    # Формируем итоговый отчёт
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"Дата ревью: {date}\n\n" + "\n\n".join(results)
    return report
