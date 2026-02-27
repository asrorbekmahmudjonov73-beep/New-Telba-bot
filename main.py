import asyncio
import logging
import os
import sys
import re
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineQuery, InlineQueryResultVoice, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
ADMIN_ID = 1185451586

class AdminState(StatesGroup):
    waiting_for_message = State()

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
    {"id": "20", "title": "Baxtiyor o baxtiyor nima indamisan", "file_id": "AwACAgQAAxkBAANxaaBA5PgFCcRYxvNlLSfDpxFRcBgAAlsrAAKrBMhT-rTpEJD829U6BA"},
    {"id": "21", "title": "Bilasilarmi do'stlarim q...niyam bilmesilar", "file_id": "AwACAgQAAxkBAAN2aaBWrlrEAAEButzYW7V7KiEVCkZvAAI6AwACooytU98Pxk0qAnQ-OgQ"},
    {"id": "22", "title": "Qoraka keldi Gruppani qorakasi", "file_id": "AwACAgIAAxkBAAN4aaBZGidXMGoNF-Pa2nxUNjD_1noAAoIMAALxGehKF6GkRwGIAuU6BA"},
]

# --- 2. Klaviaturalar (Keyboards) ---
language_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 Uzb", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Rus", callback_data="lang_ru")
        ]
    ]
)

main_menu_uz = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Barcha ovozlar"), KeyboardButton(text="Sozlamalar")]],
    resize_keyboard=True
)

settings_menu_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 Tilni o'zgartirish")],
        [KeyboardButton(text="✍️ Admin bilan bog'lanish")],
        [KeyboardButton(text="⬅️ Ortga")]
    ],
    resize_keyboard=True
)

main_menu_ru = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Все голоса"), KeyboardButton(text="Настройки")]],
    resize_keyboard=True
)

settings_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Изменить язык")],
        [KeyboardButton(text="✍️ Связаться с админом")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

# --- 3. Handlerlar ---

# /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Welcome !\nChoose Language", reply_markup=language_menu)

# Tilni tanlash (Callback)
@dp.callback_query(F.data.startswith("lang_"))
async def select_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    if lang == "uz":
        await callback.message.answer("O'zbek tili tanlandi!", reply_markup=main_menu_uz)
    else:
        await callback.message.answer("Выбран русский язык!", reply_markup=main_menu_ru)
    await callback.answer()

# Barcha ovozlar
@dp.message(F.text.in_(["Barcha ovozlar", "Все голоса"]))
async def show_all_voices(message: types.Message):
    if message.text == "Barcha ovozlar":
        text = "Barcha ovozlar ro'yxati:\n\n"
    else:
        text = "Список всех голосов:\n\n"
    for v in all_voices:
        text += f"/{v['id']}. {v['title']}\n"
    await message.answer(text)

# Maxsus ovozni yuborish (Regex)
@dp.message(F.text.regexp(r"^/(\d+)$"))
async def send_specific_voice(message: types.Message):
    voice_id = message.text.replace("/", "")
    voice_data = next((v for v in all_voices if v["id"] == voice_id), None)
    if voice_data:
        await message.answer_voice(voice_data["file_id"], caption=f"🎵 {voice_data['title']}")
    else:
        await message.answer("Bunday raqamli ovoz topilmadi / Голос не найден.")

# Sozlamalar
@dp.message(F.text.in_(["Sozlamalar", "Настройки"]))
async def show_settings(message: types.Message):
    if message.text == "Sozlamalar":
        await message.answer("Sozlamalar bo'limi:", reply_markup=settings_menu_uz)
    else:
        await message.answer("Раздел настроек:", reply_markup=settings_menu_ru)

# Ortga qaytish
@dp.message(F.text.in_(["⬅️ Ortga", "⬅️ Назад"]))
async def go_back(message: types.Message):
    if message.text == "⬅️ Ortga":
        await message.answer("Asosiy menyu", reply_markup=main_menu_uz)
    else:
        await message.answer("Главное меню", reply_markup=main_menu_ru)

# Tilni o'zgartirish
@dp.message(F.text.in_(["🇺🇿 Tilni o'zgartirish", "🇷🇺 Изменить язык"]))
async def change_lang(message: types.Message):
    await message.answer("Choose Language / Выберите язык", reply_markup=language_menu)

# Admin bilan bog'lanish - BOSHLASH
@dp.message(F.text.in_(["✍️ Admin bilan bog'lanish", "✍️ Связаться с админом"]))
async def admin_contact_start(message: types.Message, state: FSMContext):
    txt = "Xabaringizni yozing. Admin ko'rib chiqadi.\nBekor qilish uchun: /cancel" if "bog'lanish" in message.text else "Напишите сообщение. Админ рассмотрит.\nДля отмены: /cancel"
    await message.answer(txt)
    await state.set_state(AdminState.waiting_for_message)

# Admin bilan bog'lanish - XABARNI YUBORISH
@dp.message(AdminState.waiting_for_message)
async def admin_message_forward(message: types.Message, state: FSMContext):
    if message.text == "/cancel":
        await state.clear()
        await message.answer("Bekor qilindi / Отменено", reply_markup=main_menu_uz)
        return
    
    # Adminga yo'naltirish
    await bot.forward_message(chat_id=ADMIN_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    await message.answer("Xabaringiz yuborildi! ✅ / Сообщение отправлено! ✅")
    await state.clear()
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
















