import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- መረጃዎች ---
API_TOKEN = "7735268830:AAHQBAzuHJ33uMr-A34vPSEDmvXmDg21Yg0"
CHANNEL_USERNAME = "@toksavehub"
GROUP_ID = -1002444390771

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ቻናሉን Join ማድረጋቸውን መፈተሻ
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# 1. አዲስ ሰው በሊንክ ሲመጣ (Join Request)
@dp.chat_join_request_handler()
async def handle_join_request(update: types.ChatJoinRequest):
    user_id = update.from_user.id
    if await is_subscribed(user_id):
        await update.approve()
    else:
        # እዚህ ጋር "ተቀላቅለህ" ተብሎ ተስተካክሏል
        await bot.send_message(user_id, f"ሰላም {update.from_user.first_name}👋\n\nወደ ግሩፑ ለመቀላቀል መጀመሪያ ቻናላችንን መቀላቀል አለብህ።\n\nቻናሉ፡ {CHANNEL_USERNAME}\n\nተቀላቅለህ ስትጨርስ በድጋሚ የመግቢያ ጥያቄ ላክ።")

# 2. ሊንክ ሲለጥፉ መፈተሻ
@dp.message_handler()
async def filter_links(message: types.Message):
    user_id = message.from_user.id
    chat_member = await message.chat.get_member(user_id)
    if chat_member.is_chat_admin(): return

    if "t.me" in message.text.lower() or "http" in message.text.lower():
        if not await is_subscribed(user_id):
            await message.delete()
            # እዚህ ጋርም መልዕክቱ ተስተካክሏል
            await message.answer(f"❌ {message.from_user.first_name}፣ ሊንክ ለመለጠፍ መጀመሪያ {CHANNEL_USERNAME} ቻናልን መቀላቀል (Join ማድረግ) አለብህ።")

# 3. ለግሩፕና ቻናል እድገት በየሰዓቱ የሚላክ መልዕክት
async def auto_promo():
    while True:
        await asyncio.sleep(3600)
        promo = "🚀 ቻናላችንንና ግሩፓችንን ለማሳደግ @toksavehub ን ይቀላቀሉ! ጠቃሚ መረጃዎችን ያገኛሉ።"
        try:
            await bot.send_message(GROUP_ID, promo)
        except:
            pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(auto_promo())
    executor.start_polling(dp, skip_updates=True)
