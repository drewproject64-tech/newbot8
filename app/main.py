import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BotCommand,
    BotCommandScopeDefault,
    CallbackQuery,
    Message,
)

from app.config import load_config
from app.keyboards import back_menu, main_menu, sort_menu
from app.text_utils import clean_text, count_text, sort_words

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
log = logging.getLogger(__name__)

ABOUT = "Word and text tools for sorting, counting, and cleaning text."
DESCRIPTION = (
    "SB24 provides simple word and text tools directly in Telegram. "
    "Sort words, count text, or clean extra spaces with a few taps."
)
WELCOME = (
    "👋 Welcome to SB24!\n\n"
    "Work with words and text directly in Telegram. Choose a tool below."
)

class Form(StatesGroup):
    waiting_sort = State()
    waiting_count = State()
    waiting_clean = State()

async def configure_bot(bot: Bot) -> None:
    await bot.set_my_name(name="SB24")
    await bot.set_my_short_description(short_description=ABOUT)
    await bot.set_my_description(description=DESCRIPTION)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Open the main menu"),
            BotCommand(command="help", description="Show how to use SB24"),
        ],
        scope=BotCommandScopeDefault(),
    )

async def edit_to_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(WELCOME, reply_markup=main_menu())
    await callback.answer()

async def main() -> None:
    config = load_config()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await message.answer(WELCOME, reply_markup=main_menu())

    @dp.message(Command("help"))
    async def help_handler(message: Message, state: FSMContext) -> None:
        await state.clear()
        await message.answer(
            "Choose one of the three tools, then send the text you want to process. "
            "Results are returned directly in Telegram.",
            reply_markup=main_menu(),
        )

    @dp.callback_query(F.data == "menu")
    async def menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
        await edit_to_menu(callback, state)

    @dp.callback_query(F.data == "sort")
    async def sort_handler(callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(Form.waiting_sort)
        await state.update_data(sort_reverse=False)
        await callback.message.edit_text(
            "🔤 Sort Words\n\nChoose an order, then send the words or text to sort.",
            reply_markup=sort_menu(),
        )
        await callback.answer()

    @dp.callback_query(F.data.in_({"sort_az", "sort_za"}))
    async def sort_order_handler(callback: CallbackQuery, state: FSMContext) -> None:
        if await state.get_state() != Form.waiting_sort.state:
            await callback.answer("Start sorting from the main menu.", show_alert=True)
            return
        reverse = callback.data == "sort_za"
        await state.update_data(sort_reverse=reverse)
        await callback.message.edit_text(
            f"Send your words now. They will be sorted {'Z–A' if reverse else 'A–Z'}.",
            reply_markup=back_menu(),
        )
        await callback.answer()

    @dp.callback_query(F.data == "count")
    async def count_handler(callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(Form.waiting_count)
        await callback.message.edit_text(
            "🔢 Count Words\n\nSend the text you want to count.",
            reply_markup=back_menu(),
        )
        await callback.answer()

    @dp.callback_query(F.data == "clean")
    async def clean_handler(callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(Form.waiting_clean)
        await callback.message.edit_text(
            "✏️ Clean Text\n\nSend the text you want to clean.",
            reply_markup=back_menu(),
        )
        await callback.answer()

    @dp.message(Form.waiting_sort)
    async def process_sort(message: Message, state: FSMContext) -> None:
        text = message.text or ""
        data = await state.get_data()
        reverse = bool(data.get("sort_reverse", False))
        result = sort_words(text, reverse=reverse)
        if not result:
            await message.answer("Please send some words or text to sort.", reply_markup=back_menu())
            return
        await message.answer(
            f"🔤 Sorted {'Z–A' if reverse else 'A–Z'}:\n\n{result}",
            reply_markup=back_menu(),
        )
        await state.clear()

    @dp.message(Form.waiting_count)
    async def process_count(message: Message, state: FSMContext) -> None:
        text = message.text or ""
        words, chars, non_space = count_text(text)
        if chars == 0:
            await message.answer("Please send some text to count.", reply_markup=back_menu())
            return
        await message.answer(
            "🔢 Text Count\n\n"
            f"Words: {words}\n"
            f"Characters: {chars}\n"
            f"Characters without spaces: {non_space}",
            reply_markup=back_menu(),
        )
        await state.clear()

    @dp.message(Form.waiting_clean)
    async def process_clean(message: Message, state: FSMContext) -> None:
        text = message.text or ""
        result = clean_text(text)
        if not result:
            await message.answer("Please send some text to clean.", reply_markup=back_menu())
            return
        await message.answer(f"✏️ Cleaned Text:\n\n{result}", reply_markup=back_menu())
        await state.clear()

    @dp.message()
    async def fallback(message: Message) -> None:
        await message.answer(
            "Please choose one of SB24's three tools from the menu below.",
            reply_markup=main_menu(),
        )

    await configure_bot(bot)
    me = await bot.get_me()
    log.info("Starting @%s", me.username)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
