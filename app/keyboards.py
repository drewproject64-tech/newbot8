from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔤 Sort Words", callback_data="sort"),
            InlineKeyboardButton(text="🔢 Count Words", callback_data="count"),
        ],
        [InlineKeyboardButton(text="✏️ Clean Text", callback_data="clean")],
    ])

def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Main Menu", callback_data="menu")],
    ])

def sort_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="A–Z", callback_data="sort_az"),
            InlineKeyboardButton(text="Z–A", callback_data="sort_za"),
        ],
        [InlineKeyboardButton(text="🏠 Main Menu", callback_data="menu")],
    ])
