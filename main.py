import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from bot.handlers import handle_zip

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# Регистрация обработчиков
@dp.message(Command(commands=["start"]))
async def handle_start(message):
    await message.answer("Привет! Отправьте ZIP-архив для анализа.")


@dp.message(
    lambda message: message.document
    and message.document.mime_type == "application/zip"
)
async def handle_document(message):
    await handle_zip(message, bot)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
