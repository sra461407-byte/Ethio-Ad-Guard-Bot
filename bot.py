import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- መረጃዎች ---
API_TOKEN = "7735268830:AAHQBAzuHJ33uMr-A34vPSEDmvXmDg21Yg0"
CHANNEL_USERNAME = "@TokSaveHub"  # ያንተ የቻናል ስም
GROUP_ID = -1002444390771        # ያንተ የግሩፕ ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- ቻናሉን Join ማድረጋቸውን መፈተሻ ---
async def is_subscribed(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# --- 1. አዲስ ሰው በሊንክ ሲመጣ (Join Request) ---
@dp.chat_join_request_handler()
async def handle_join_request(update: types.ChatJoinRequest):
    user_id = update.from_user.id
    if await is_subscribed(user_id):
        await update.approve() # ቻናሉ ውስጥ ካለ ይቀበለዋል
    else:
        # ካልሆነ መመሪያ ይልክለታል
        await bot.send_message(user_id, f"ሰላም {update.from_user.first_name}👋\n\nወደ ግሩፑ ለመቀላቀል መጀመሪያ ቻናላችንን መቀላቀል አለብህ።\n\nቻናሉ፡ {CHANNEL_USERNAME}\n\nቀላቅለህ ስትጨርስ በድጋሚ የመግቢያ ጥያቄ ላክ።")

# --- 2. ሊንክ ሲለጥፉ መፈተሻ ---
@dp.message_handler()
async def filter_links(message: types.Message):
    user_id = message.from_user.id
    chat_member = await message.chat.get_member(user_id)
    
    # አድሚን ከሆነ ምንም አይከለከልም
    if chat_member.is_chat_admin(): return

    # መልዕክቱ ውስጥ ሊንክ ካለ ብቻ ይፈትሻል
    if "t.me" in message.text.lower() or "http" in message.text.lower():
        if not await is_subscribed(user_id):
            await message.delete()
            await message.answer(f"❌ {message.from_user.first_name}፣ ሊንክ ለመለጠፍ መጀመሪያ ቻናላችንን መቀላቀል አለብህ፡ {CHANNEL_USERNAME}")

# --- 3. በየሰዓቱ የሚለጠፍ ማስታወቂያ (ለቻናል እድገት) ---
async def auto_promo():
    while True:
        await asyncio.sleep(3600) # በየ 1 ሰዓቱ
        promo_text = (
            "🚀 **ቻናላችንን ይቀላቀሉ!**\n\n"
            "ጠቃሚ መረጃዎችን እና የቲክቶክ ቪዲዮ ማውረጃ ቦቶችን ለማግኘት @TokSaveHub ን Join ያድርጉ።"
        )
        try:
            await bot.send_message(GROUP_ID, promo_text)
        except:
            pass

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(auto_promo())
    executor.start_polling(dp, skip_updates=True)
