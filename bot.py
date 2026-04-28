import os
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# ያንተ Token እዚህ ገብቷል
API_TOKEN = "7735268830:AAHQBAzuHJ33uMr-A34vPSEDmvXmDg21Yg0"
REQUIRED_ADD = 5 
DATA_FILE = "user_data.json"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ዳታውን ለማንበብ
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

# ዳታውን ለማስቀመጥ
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def on_user_added(message: types.Message):
    adder_id = str(message.from_user.id)
    added_count = len(message.new_chat_members)
    
    data = load_data()
    data[adder_id] = data.get(adder_id, 0) + added_count
    save_data(data)
    
    current = data[adder_id]
    if current < REQUIRED_ADD:
        await message.answer(f"🙏 {message.from_user.first_name}፣ እስካሁን {current} ሰው ጨምረሃል። ሊንክ ለመለጠፍ {REQUIRED_ADD - current} ሰው ይቀረሃል!")
    else:
        await message.answer(f"✅ እንኳን ደስ አለህ! {REQUIRED_ADD} ሰው ስለሞላህ አሁን ማስታወቂያ መለጠፍ ትችላለህ።")

@dp.message_handler(lambda message: "t.me" in message.text.lower() or "http" in message.text.lower())
async def filter_links(message: types.Message):
    user_id = str(message.from_user.id)
    chat_member = await message.chat.get_member(user_id)
    
    if chat_member.is_chat_admin(): return

    data = load_data()
    user_adds = data.get(user_id, 0)
    
    if user_adds < REQUIRED_ADD:
        await message.delete()
        await message.answer(f"❌ ይቅርታ {message.from_user.first_name}፣ ሊንክ ለመለጠፍ መጀመሪያ {REQUIRED_ADD} ሰው መጨመር አለብህ። (ያለህ: {user_adds})")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
