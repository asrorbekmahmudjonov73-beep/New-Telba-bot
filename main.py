import asyncio
import logging
import os
import sys
import re
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineQuery, InlineQueryResultVoice, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# 1. Bot sozlamalari
TOKEN = os.getenv("TOKEN") 
bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 2. Ovozlar ro'yxati
all_voices = [
    {"id": "1", "title": "Haydelar", "file_id": "AwACAgQAAxkBAAMraZIyb_9L6kLbApOLoSmypRV7XD4AAgwcAALVgVFQ-5vxHXZ_I5Y6BA"},
    {"id": "2", "title": "Meni chaqirib, o'zlaring yoqsanlar", "file_id": "AwACAgQAAxkBAAMtaZIy6KTFhtUa4Yh8TiooV8ceI1wAAj8fAAL0VGBQ25_d8sbzMlc6BA"},
    {"id": "3", "title": "bir narsa qimimizmi, tashkillashtirmimzmi ?", "file_id": "AwACAgQAAxkBAAMvaZIzFDUB4xjcQNd2JZhBi5N83WYAAkEfAAL0VGBQU2kF05FKze46BA"},
    {"id": "4", "title": "Rassa joyi bo'lyaptida dos maydalab", "file_id": "AwACAgQAAxkBAAMxaZIzG7DsHlMZxaeountGAqBSREgAAlobAAICAAFwUNiSUqHDnVAjOgQ"},
    {"id": "5", "title": "Toshkenda 10 paqir yomg'ir", "file_id": "AwACAgQAAxkBAAMzaZIzKRxsTW5JEZC93EdaNFyzbLcAAqgdAAIx9pFQbSkAAdz5dvGOOgQ"},
    {"id": "6", "title": "Kettik bugun yakshanbayu", "file_id": "AwACAgQAAxkBAAM1aZIzMoIrxxxLahgzJF8SNL6LORcAAqkdAAIx9pFQVtpqBNHttv46BA"},
    {"id": "7", "title": "gosht ye gosht", "file_id": "AwACAgQAAxkBAAM3aZIzOiFQ9sWdz5CJ2MNzCAFqH-YAAqodAAIx9pFQsbcuLhN9aoc6BA"},
    {"id": "8", "title": "Arbialomisan ??", "file_id": "AwACAgQAAxkBAAM5aZIzQkp5JdGlFNBylVYu-tWJRWMAAqsdAAIx9pFQnBSRHBFZSuM6BA"},
    {"id": "9", "title": "Octagon pactagon qilishma", "file_id": "AwACAgQAAxkBAAM7aZIzSqARCZcZgp3BAmjqx5_7wM4AAqwdAAIx9pFQ-symnmvxd_E6BA"},
    {"id": "10", "title": "Men kochadaman, senlar qayerdasan", "file_id": "AwACAgQAAxkBAAM9aZIzUmW-p-iw744qds7Ni8vxubsAAq4dAAIx9pFQ9GnkII73uWk6BA"},
    {"id": "11", "title": "Senlar bugun bayramniyam kotinga tiqasan", "file_id": "AwACAgQAAxkBAAM_aZIzWYPEEcJgVIFgKD7sWYnpTjgAAq8dAAIx9pFQLMoDyZI36Mo6BA"},
    {"id": "12", "title": "kesen kelish ee", "file_id": "AwACAgQAAxkBAANBaZIzYI0dOkjzSJKI5sI2XA2UU_AAArAdAAIx9pFQ1QFoW1zk4iI6BA"},
    {"id": "13", "title": "Xabi Alonso kuydirdinku", "file_id": "AwACAgQAAxkBAANDaZIzZp7EAAFQc7e_iyzw6m3OOdCTAAKxHQACMfaRULzprRJFzi-COgQ"},
    {"id": "14", "title": "Kot boldi, kot boldi", "file_id": "AwACAgQAAxkBAANFaZIzbAYkrCZvS00qSfCuMgJvwzIAArIdAAIx9pFQQhIJzjZ7lB46BA"},
    {"id": "15", "title": "Xabi Alonso somseni yuvib bording", "file_id": "AwACAgQAAxkBAANHaZIzcg5Zhahp2K1PIXGF3n9c86gAArQdAAIx9pFQ4qc3C0KFGvI6BA"},
    {"id": "16", "title": "Trend Aliksandor biladi u", "file_id": "AwACAgQAAxkBAANJaZIzeLRXko7Uz3vYm48hm10I_0IAArUdAAIx9pFQZtJ0OcowF4Q6BA"},
    {"id": "17", "title": "Arda guler...", "file_id": "AwACAgQAAxkBAANNaZIzhXFLJrJvL3YfkgKz_4VtZZAAArgdAAIx9pFQPLsHuBFhSPs6BA"},
    {"id": "18", "title": "Turinglar ee soat 8:30 bolyapti", "file_id": "AwACAgQAAxkBAANPaZIzoA5GRjLOqY3oL6DY3U9ESzEAArkdAAIx9pFQT1Z_OqjVU1A6BA"},
    {"id": "19", "title": "Assalomu allaykum Juma ayyom", "file_id": "AwACAgQAAxkBAANVaZIztrfYV7XQ6hbeH3lkInuYn_sAArwdAAIx9pFQK4VMQxvgEAo6BA"},
]

# 3. Tugmalar (Keyboard)
main_menu = ReplyKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="uz UZB", callback_data="lang_uz"), 
            InlineKeyboardButton(text="ru Rus", callback_data="lang_ru")
        ]
    ],   
)
# 4. Handlerlar

# /start komandasi
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Welcome !\nChoose Language",
        reply_markup=main_menu
    )

@dp.callback_query(F.date.startswith("Lang_"))
async def select_language(callback: types.CallbackQuery):
    # Foydalanuvchi qaysi tilni tanlaganini aniqlaymiz (ixtiyoriy)
 lang = callback.data.split("_")[1]

if lang == "uz":
    await callback.message.answer("O'zbek tili tanlandi!", reply_markup=main_menu)
    else:
        await callback.message.answer("Выбран русский язык!", reply_markup=main_menu)
    
    # Soat belgisi (loading) aylanishini to'xtatish uchun
    await callback.answer()

# "Barcha ovozlar" tugmasi bosilganda
@dp.message(F.text == "Barcha ovozlar")
async def show_all_voices(message: types.Message):
    text = "Siz uchun barcha ovozlar ro'yxati:\n\n"
    for v in all_voices:
        # Har bir ovozni /1, /2 ko'rinishida chiqaradi
        text += f"/{v['id']}. {v['title']}\n"
    await message.answer(text)

# "/1", "/2" kabi buyruqlar kelganda ovozni yuborish
@dp.message(F.text.regexp(r"^/(\d+)$"))
async def send_specific_voice(message: types.Message):
    # Raqamni ajratib olamiz (masalan "/5" -> "5")
    voice_id = message.text.replace("/", "")
    
    # Ro'yxatdan o'sha ID ga mos ovozni qidiramiz
    voice_data = next((v for v in all_voices if v["id"] == voice_id), None)
    
    if voice_data:
        await message.answer_voice(
            voice_data["file_id"],
            caption=f"Ovoz: {voice_data['title']}"
        )
    else:
        await message.answer("Bunday raqamli ovoz topilmadi.")

# "Sozlamalar" tugmasi
@dp.message(F.text == "Sozlamalar")
async def settings(message: types.Message):
    await message.answer("Sozlamalar bo'limi hozircha tayyor emas.")

# 🎤 Yangi ovozlar uchun file_id olish
@dp.message(F.voice)
async def get_voice_id(message: types.Message):
    file_id = message.voice.file_id
    await message.answer(f"Yangi ovoz ID-si:\n<code>{file_id}</code>", parse_mode="HTML")

# 🔍 Inline Query
@dp.inline_query()
async def inline_handler(query: InlineQuery):
    results = []
    search_text = query.query.lower()
    for v in all_voices:
        if search_text in v["title"].lower():
            results.append(
                InlineQueryResultVoice(
                    id=v["id"], 
                    voice_url=v["file_id"], 
                    title=v["title"]
                )
            )
    await query.answer(results[:50], cache_time=0, is_personal=True)

# 5. Web Server (Cron-job va Render uchun)
async def handle(request):
    return web.Response(text="Bot ishlayapti!")

async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def main():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    
    await asyncio.gather(site.start(), start_bot())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass




