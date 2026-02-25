import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Update

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_HOST = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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

# =========================
# INLINE HANDLER (O'ZGARMADI)
# =========================

# 🎤 Voice handler
@dp.message(F.voice)
async def handle_voice(message: types.Message):
    await message.answer("Ovozli xabar qabul qilindi 🎤")

# Webhook handler
async def handle(request):
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return web.Response()

# Startup
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    print("Webhook o‘rnatildi:", WEBHOOK_URL)

# Shutdown
async def on_shutdown(app):
    await bot.delete_webhook()

def main():
    app = web.Application()
    app.router.add_post(WEBHOOK_PATH, handle)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    port = int(os.getenv("PORT", 10000))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
