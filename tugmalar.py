from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📌 E'lon joylash", callback_data="adv")],
        [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")],
        [InlineKeyboardButton(text="🔗 Barcha e'lonlar", url="https://olx.uz/")]
    ]
)

phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Raqam yuborish", request_contact=True)]
    ],
    resize_keyboard=True
)

confirm_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Ha"), KeyboardButton(text="❌ Yo'q")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)