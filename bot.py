import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- መረጃዎች ---
API_TOKEN = '7735268830:AAHQBAzuHJ33uMr-A34vPSEDmvXmDg21Yg0'
GROUP_ID = -1002444390771 # በትክክለኛው የግሩፕ ID ተክቼዋለሁ
TIKTOK_BOT = "@TokSaverXBot"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- 1. አዲስ ሰው ሲገባ ሰላምታ እና ማስታወቂያ ---
@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def welcome_member(message: types.Message):
    for new_user in message.new_chat_members:
        welcome_text = (
            f"ሰላም {new_user.first_name}! 👋\n"
            f"እንኳን ወደ {message.chat.title} በሰላም መጡ።\n\n"
            f"📌 እዚህ ግሩፕ ላይ በነጻ ማስተዋወቅ ይችላሉ!\n"
            f"🔥 የቲክቶክ ቪዲዮ ያለ watermark ለማውረድ የኛን ቦት ይጠቀሙ፡ {TIKTOK_BOT}"
        )
        await message.reply(welcome_text)

# --- 2. ሊንክ የሚለጥፉ ሰዎችን መቆጣጠር (Anti-Link) ---
@dp.message_handler(lambda message: "t.me" in message.text.lower() or "http" in message.text.lower())
async def handle_links(message: types.Message):
    user_id = message.from_user.id
    chat_member = await message.chat.get_member(user_id)
    
    # አድሚን ካልሆነ ሊንኩን ያጠፋል
    if not chat_member.is_chat_admin():
        await message.delete()
        await message.answer(f"ይቅርታ {message.from_user.first_name}፣ ማስታወቂያ መለጠፍ የሚቻለው ያለ ሊንክ ብቻ ነው! ❌")

# --- 3. በየ 1 ሰዓቱ የቲክቶክ ቦቱን በራስ ሰር ማስተዋወቅ ---
async def scheduled_ad():
    while True:
        # በየ 3600 ሰከንድ (1 ሰዓት) ማስታወቂያ ይለጥፋል
        await asyncio.sleep(3600) 
        ad_text = (
            "🌟 **ጠቃሚ መረጃ ለቲክቶክ ተጠቃሚዎች!** 🌟\n\n"
            "የቲክቶክ ቪዲዮዎችን ያለ watermark በፍጥነት ለማውረድ @TokSaverXBot ን ይጠቀሙ።\n"
            "በጣም ቀላል እና ፈጣን ነው! 👇\n\n"
            "👉 @TokSaverXBot"
        )
        try:
            await bot.send_message(chat_id=GROUP_ID, text=ad_text, parse_mode='Markdown')
        except Exception as e:
            print(f"Error sending ad: {e}")

# --- ቦቱን የሚያስጀምር ክፍል ---
if __name__ == '__main__':
    # ማስታወቂያውን በ background እንዲጀምር ያደርጋል
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled_ad())
    
    # ቦቱን ያስነሳል
    executor.start_polling(dp, skip_updates=True)
