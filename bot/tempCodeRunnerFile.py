import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ContentType
from aiogram.filters import Command
from dotenv import load_dotenv
from bot.handlers import handle_start, handle_zip
import logging


import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


logging.basicConfig(level=logging.DEBUG)


# Загружаем переменные окружения
load_dotenv()

# Настройки бота
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# Регистрация обработчиков
@dp.message(Command(commands=["start"]))
async def start_handler(message):
    """Обработчик команды /start"""
    await handle_start(message)


@dp.message(
    lambda message: message.document
    and message.document.mime_type == "application/zip"
)
async def zip_handler(message):
    """Обработчик ZIP-архивов"""
    await handle_zip(message, bot)


async def main():
    """Запуск бота"""
    await bot.delete_webhook(
        drop_pending_updates=True
    )  # Сбрасываем старые обновления
    await dp.start_polling(bot)  # Запускаем long polling


if __name__ == "__main__":
    asyncio.run(main())
