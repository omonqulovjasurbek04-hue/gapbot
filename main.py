
import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import (
    Message,
    BotCommand,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)

from dotenv import load_dotenv
import edge_tts

load_dotenv()
TOKEN = os.getenv("API")

dp = Dispatcher()

async def defoult(bot: Bot):
    commands = [
        BotCommand(command="start", description="Boshlab beradi"),
        BotCommand(command="help", description="Yordam uchun"),
        BotCommand(command="about", description="Bot haqida")
    ]
    await bot.set_my_commands(commands)

menu = {
    "👨‍🦰 Sardor 🇺🇿": "uz-UZ-SardorNeural",
    "👩 Madina 🇺🇿": "uz-UZ-MadinaNeural",
    "👨‍🦱 Ahmet 🇹🇷": "tr-TR-AhmetNeural",
    "👩 Emel 🇹🇷": "tr-TR-EmelNeural",
    "👨‍🦰 Dmitry 🇷🇺": "ru-RU-DmitryNeural",
    "👩 Svetlana 🇷🇺": "ru-RU-SvetlanaNeural",
    "👩‍🦰 Dariya 🇷🇺": "ru-RU-DariyaNeural",
    "🤖 Neural 🇺🇸": "en-US-GuyNeural",
    "👨 Andrew 🇺🇸": "en-US-AndrewNeural",
    "👨 Brian 🇺🇸": "en-US-BrianNeural",
    "👨 Eric 🇺🇸": "en-US-EricNeural",
    "👨 Roger 🇺🇸": "en-US-RogerNeural",
    "👨 Steffan 🇺🇸": "en-US-SteffanNeural",
    "👨 Christopher 🇺🇸": "en-US-ChristopherNeural",
    "👩 Ava 🇺🇸": "en-US-AvaNeural",
    "👩 Emma 🇺🇸": "en-US-EmmaNeural",
    "👩 Jenny 🇺🇸": "en-US-JennyNeural",
    "👩 Michelle 🇺🇸": "en-US-MichelleNeural",
    "👩 Aria 🇺🇸": "en-US-AriaNeural",
    "👩 Ana 🇺🇸": "en-US-AnaNeural",
    "👨 Ryan 🇬🇧": "en-GB-RyanNeural",
    "👩 Sonia 🇬🇧": "en-GB-SoniaNeural",
    "👨 Brian 🇬🇧": "en-GB-BrianNeural",
    "👨‍🦱 Hamed 🇸🇦": "ar-SA-HamedNeural",
    "👩‍🦱 Zariyah 🇸🇦": "ar-SA-ZariyahNeural"
}

def ta2(lst):
    return [lst[i:i + 2] for i in range(0, len(lst), 2)]

buttons = [KeyboardButton(text=k) for k in menu]
Menu = ReplyKeyboardMarkup(keyboard=ta2(buttons), resize_keyboard=True)

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        f"Salom, {html.bold(message.from_user.full_name)}!\nMenu tanlang ⬇️",
        reply_markup=Menu
    )

tel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Murojaat", url="https://t.me/itlive_09")]
    ]
)

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        f"Salom, {html.bold(message.from_user.full_name)}!\nYordam uchun murojaat qiling",
        reply_markup=tel
    )

@dp.message(Command("about"))
async def about_cmd(message: Message):
    await message.answer(
        f"Salom, {html.bold(message.from_user.full_name)}!\nMatn ➜ Ovoz bot"
    )

users = {}

async def ovoz(text, filename, voice):
    max_len = 300
    parts = [text[i:i + max_len] for i in range(0, len(text), max_len)]
    files = []

    for i, part in enumerate(parts):
        temp = f"part_{i}.mp3"
        tts = edge_tts.Communicate(part, voice)
        await tts.save(temp)
        files.append(temp)

    with open(filename, "wb") as out:
        for f in files:
            with open(f, "rb") as p:
                out.write(p.read())
            os.remove(f)

@dp.message(F.text.in_(menu.keys()))
async def choose_voice(message: Message):
    T = message.text
    users[message.from_user.id] = menu[T]

    if "👨" in T or "🤖" in T:
        gender_emoji = "🧔 Erkak"
    elif "👩" in T:
        gender_emoji = "👩 Ayol"
    else:
        gender_emoji = "👤 Foydalanuvchi"

    await message.answer(
        f"✅ {gender_emoji} ovoz tanlandi ({T})\nEndi matn yuboring."
    )

@dp.message(F.text)
async def handler(message: Message):
    if message.from_user.id not in users:
        await message.answer("Avval ovoz tanlang: /start")
        return

    text = message.text.strip()
    if not text:
        await message.answer("Matn bo‘sh bo‘lmasin")
        return

    voice = users[message.from_user.id]
    filename = f"voice_{message.chat.id}_{message.message_id}.mp3"


    try:
        await ovoz(text, filename, voice)
        await message.answer_voice(FSInputFile(filename), caption="Tayyor")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

async def main():
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await defoult(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
