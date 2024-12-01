from reportlab.pdfgen import canvas
from bot.utils import process_zip_file
from api.client import get_review
from aiogram.types import FSInputFile
from reports.pdf_generator import generate_pdf
import os


async def handle_zip(message, bot):
    """Обработка ZIP-архивов и генерация ревью."""
    document = message.document
    if not document.file_name.endswith(".zip"):
        await message.answer("Пожалуйста, отправьте ZIP-архив.")
        return

    # Загрузка файла
    file = await bot.download(document.file_id)
    file_content = file.read()

    # Обработка ZIP-архива
    files_content = process_zip_file(file_content)

    if not files_content:
        await message.answer("Не удалось извлечь текстовые данные из архива.")
        return

    review_content = []

    for file_name, content in files_content.items():
        # Запрос к API
        review = await get_review(content, rules=[])
        review_content.append(f"Файл: {file_name}\n{review}\n")

    # Генерация PDF
    pdf_path = "review.pdf"
    generate_pdf(review_content, pdf_path)  # Убираем время из каждой строки

    # Отправка PDF пользователю
    await bot.send_document(message.chat.id, FSInputFile(pdf_path))

    # Удаление временного файла
    os.remove(pdf_path)
