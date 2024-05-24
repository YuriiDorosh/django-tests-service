import asyncio
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv
import os
import aiohttp
import logging

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot_activity.log",
    filemode="a",
)
logger = logging.getLogger(__name__)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    logger.info(
        f"User {message.from_user.id} - {message.from_user.username} executed /start"
    )
    welcome_message = (
        "Використовуйте /set <url> | <button>, щоб встановити налаштування.\n"
        "Використовуйте /runtests, щоб запустити тести.\n"
        "Використовуйте /settings, щоб переглянути поточні налаштування."
    )
    await message.reply(welcome_message)


@dp.message_handler(commands=["set"])
async def set_settings(message: types.Message):
    logger.info(
        f"User {message.from_user.id} - {message.from_user.username} attempted to set settings with {message.text}"
    )
    try:
        _, settings = message.text.split(" ", 1)
        url, button = settings.split("|")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://backend:8000/api/v1/tests/set/",
                data={"url": url.strip(), "button": button.strip()},
            ) as response:
                if response.status == 200:
                    logger.info(
                        f"Settings updated successfully by user {message.from_user.id}"
                    )
                    await message.reply("Налаштування успішно оновлено!")
                else:
                    logger.warning(
                        f"Failed to update settings for user {message.from_user.id} with response {response.status}"
                    )
                    await message.reply("Не вдалося оновити налаштування.")
    except Exception as e:
        logger.error(
            f"Exception in /set command by user {message.from_user.id}: {str(e)}"
        )
        await message.reply(f"Помилка: {str(e)}")


@dp.message_handler(commands=["settings"])
async def get_settings(message: types.Message):
    logger.info(
        f"User {message.from_user.id} - {message.from_user.username} requested settings"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get("http://backend:8000/api/v1/tests/get/") as response:
            if response.status == 200:
                settings = await response.json()
                settings_message = f"Поточні налаштування:\nURL: {settings['url']}\nКнопка: {settings['button']}"
                await message.reply(settings_message)
            else:
                logger.warning(
                    f"Failed to retrieve settings for user {message.from_user.id} with status {response.status}"
                )
                await message.reply(
                    f"Не вдалося отримати налаштування. Статус: {response.status}"
                )


@dp.message_handler(commands=["runtests"])
async def run_tests(message: types.Message):
    logger.info(
        f"User {message.from_user.id} - {message.from_user.username} initiated a test run"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get("http://backend:8000/api/v1/tests/test") as response:
            if response.status == 200:
                result = await response.json()
                if "errors" in result and result["errors"]:
                    errors = result["errors"]
                    logger.error(f"Tests failed with errors: {errors}")
                    await message.reply(f"Тести не пройшли. Помилки: {errors}")
                else:
                    logger.info(
                        f"Test run successfully for user {message.from_user.id}"
                    )
                    await message.reply(f"Результат тесту: {result['data']}")
            else:
                logger.error(
                    f"Failed to run tests for user {message.from_user.id} with status {response.status}"
                )
                await message.reply(
                    f"Не вдалося виконати тести. Статус: {response.status}"
                )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
