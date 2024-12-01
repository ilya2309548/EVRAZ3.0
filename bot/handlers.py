from bot.utils import process_zip_file
from api.client import send_to_llm


async def handle_start(message):
    """Обработчик команды /start"""
    await message.answer("Привет! Отправьте ZIP-архив для анализа.")


async def handle_zip(message, bot):
    """Обработка ZIP-архивов"""
    document = message.document
    if not document.file_name.endswith(".zip"):
        await message.answer("Пожалуйста, отправьте ZIP-архив.")
        return

    # Загрузка файла
    file = await bot.download(document.file_id)
    file_content = file.read()

    # Обработка ZIP-архива
    files_content = process_zip_file(file_content)

    # Отправка данных в LLM
    response = await send_to_llm(files_content)
    assistant_response = (
        response.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "Нет ответа.")
    )

    await message.answer(f"Ответ от модели:\n{assistant_response}")
