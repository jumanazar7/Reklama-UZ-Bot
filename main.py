import re
import logging
from config import TOKEN, ADMIN_ID
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from database import insert_user, insert_adv, adv_table_create
from tugmalar import main_menu, phone_number, confirm_buttons
from states import AdvStates
from aiogram.types import ReplyKeyboardRemove


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
# adv_table_create(path="D:/Python808/BOT/databases/users.db")

@dp.message_handler(commands=["start"], state="*")
async def do_start(message: types.Message, state: FSMContext):
    await state.finish()
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    await bot.send_message(chat_id=1343692719, text=f"ID: {user_id} sizning botga start bosdi. @{message.from_user.username}")
    await message.reply(f"Salom <b>{full_name}</b>. Men sizning xizmatingizdaman 🤝 \nSizning ID: {user_id}", parse_mode="html", disable_web_page_preview=True, reply_markup=main_menu)
    try:
        insert_user(path='D:/Python808/BOT/databases/users.db',tg_id=user_id, full_name=full_name, username=message.from_user.username)
    except Exception as e:
        print(e)

@dp.callback_query_handler(text="adv")
async def get_adv(call: types.CallbackQuery):
    await call.answer("✔️ Barcha ma'lumotlarni to'liq to'ldiring", show_alert=True)
    await call.message.answer("✍️ Mahsulot nomini kiriting")
    await call.message.delete()
    await AdvStates.title.set()

@dp.message_handler(lambda message: isinstance(message.text, str), state=AdvStates.title)
async def get_title(message: types.Message, state: FSMContext):
    title = message.text
    print(type(title))
    await state.update_data(
        {'title': title}
    )
    await message.answer("✏️ Mahsulot haqida batafsil ma'lumot kiriting")
    await AdvStates.next()

@dp.message_handler(state=AdvStates.desc)
async def get_desc(message: types.Message, state: FSMContext):
    desc = message.text
    await state.update_data(
        {'desc': desc}
    )
    await message.answer("📸 Mahsulot rasmini jo'nating")
    await AdvStates.next()

@dp.message_handler(content_types=['photo'], state=AdvStates.image)
async def get_image_id(message: types.Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    await state.update_data(
        {'image_id': image_id}
    )
    await message.answer("💰 Mahsulot narxini kiriting")
    await AdvStates.price.set()

@dp.message_handler(lambda message: isinstance(message.text, str), state=AdvStates.price)
async def get_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(
            {'price': price}
        )
    except:
        await message.answer("Noto'g'ri formatda kiritmang (Exp: 12500878.99)")
        await AdvStates.price.set()
    else:
        await message.answer("Telefon raqamingizni tasdiqlang", reply_markup=phone_number)
        await AdvStates.phone.set()


@dp.message_handler(content_types=['contact'], state=AdvStates.phone)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    andoza = "(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"
    if re.match(andoza, phone):
        await state.update_data(
            {'phone': phone}
        )
        data = await state.get_data()
        title = data.get('title')
        desc = data.get('desc')
        image_id = data.get('image_id')
        price = data.get('price')
        msg = f"<b>Mahsulot nomi:</b> {title}\n<b>Batafsil ma'lumot:</b> {desc}\n<b>Mahsulot narxi:</b> {price}\n<b>Bog'lanish uchun:</b> {phone}"
        await message.answer_photo(photo=image_id, caption=msg, reply_markup=confirm_buttons, parse_mode="html")
        await AdvStates.next()
    else:
        await message.answer("Faqat o'zbekiston telefon raqamini qabul qilamiz", reply_markup=phone_number)

@dp.message_handler(state=AdvStates.confirm, text="✅ Ha")
async def save_adv(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data.get('title')
    desc = data.get('desc')
    image_id = data.get('image_id')
    price = data.get('price')
    phone = data.get('phone')
    insert_adv(path='D:/Python808/BOT/databases/users.db',tg_id=message.from_user.id, title=title, desc=desc, image=image_id, price=price, phone=phone)
    await message.answer("➕ Barcha ma'lumotlar muvaffaqiyatli saqlandi va adminga yuborildi", reply_markup=ReplyKeyboardRemove())
    await message.answer("Siz asosiy menyudasiz", reply_markup=main_menu)
    msg = f"<b>Mahsulot nomi:</b> {title}\n<b>Batafsil ma'lumot:</b> {desc}\n<b>Mahsulot narxi:</b> {price}\n<b>Bog'lanish uchun:</b> {phone}"
    await bot.send_photo(chat_id=ADMIN_ID, photo=image_id, caption=msg, parse_mode="html")
    await state.finish()

@dp.message_handler(state=AdvStates.confirm, text="❌ Yo'q")
async def cancel_adv(message: types.Message, state: FSMContext):
    await message.answer("Barcha ma'lumotlaringiz bekor qilindi", reply_markup=ReplyKeyboardRemove())
    await message.answer("Siz asosiy menyudasiz", reply_markup=main_menu)
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

