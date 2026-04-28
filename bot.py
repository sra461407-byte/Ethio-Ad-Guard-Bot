import logging
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# --- መረጃዎች ---
API_TOKEN = os.getenv('BOT_TOKEN')
GROUP_ID = -1002444390771
REQUIRED_ADD = 5  # ማስታወቂያ ለመለጠፍ መታከል ያለበት አባል ብዛት

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# የሰዎችን ዳታ ለመያዝ
DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- አዲስ ሰው ሲጨመር የሚሰራ ---
@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def on_user_added(message: types.Message):
    adder_id = str(message.from_user.id)
    added_count = len(message.new_chat_members)
    
    data = load_data()
    
    if adder_id not in data:
        data[adder_id] = 0
    
    data[adder_id] += added_count
    save_data(data)
    
    current_total = data[adder_id]
    
    if current_total < REQUIRED_ADD:
        await message.answer(f"🙏 {message.from_user.first_name}፣ እስካሁን {current_total} ሰው ጨምረሃል። ሊንክ ለመለጠፍ {REQUIRED_ADD - current_total} ሰው ይቀረሃል!")
    else:
        await message.answer(f"✅ እንኳን ደስ አለህ {message.from_user.first_name}! {REQUIRED_ADD} ሰው ስለሞላህ አሁን ማስታወቂያ መለጠፍ ትችላለህ።")

# --- ሊንክ መቆጣጠሪያ ---
@dp.message_handler(lambda message: "t.me" in message.text.lower() or "http" in message.text.lower())
async def link_filter(message: types.Message):
    user_id = str(message.from_user.id)
    chat_member = await message.chat.get_member(user_id)
    
    # አድሚን ከሆነ ይለፍ
    if chat_member.is_chat_admin():
        return

    data = load_data()
    user_adds = data.get(user_id, 0)
    
    if user_adds < REQUIRED_ADD:
        await message.delete()
        await message.answer(
            f"❌ ይቅርታ {message.from_user.first_name}፣ ሊንክ ለመለጠፍ መጀመሪያ {REQUIRED_ADD} ሰው መጨመር አለብህ።\n"
            f"አንተ እስካሁን የጨመርከው፡ {user_adds} ሰው ነው።"
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
