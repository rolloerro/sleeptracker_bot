import asyncio
import json
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "🌙 SleepTracker — персональный трекер сна\n\n"
        "Команды:\n"
        "😴 /sleep — ложусь спать\n"
        "☀️ /wake — проснулся"
    )

@dp.message(Command("sleep"))
async def sleep(msg: types.Message):
    data = load_data()
    data[str(msg.from_user.id)] = {
        "sleep_time": datetime.now().isoformat()
    }
    save_data(data)
    await msg.answer("😴 Спокойной ночи. Я засёк время сна.")

@dp.message(Command("wake"))
async def wake(msg: types.Message):
    data = load_data()
    user = data.get(str(msg.from_user.id))

    if not user or "sleep_time" not in user:
        await msg.answer("Я не нашёл запись о начале сна 🤔")
        return

    start = datetime.fromisoformat(user["sleep_time"])
    end = datetime.now()
    duration = end - start

    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60

    await msg.answer(
        f"☀️ Доброе утро!\n"
        f"Ты спал {hours}ч {minutes}м.\n"
        f"Хороший сон = энергия 💪"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
