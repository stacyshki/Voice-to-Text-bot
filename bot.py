from speech import SpeechProcessing
from text_processing import GenI
import asyncio
import logging
import json
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


load_dotenv()
TOKEN = getenv("BOT_TOKEN")
logging.basicConfig(level = logging.INFO)
bot = Bot(token = TOKEN)
dp = Dispatcher()

with open("lang.json", mode = "r", encoding = "utf-8") as read_file:
    lang = json.load(read_file)

btn_lang_en = KeyboardButton(text = "English \U0001f1ec\U0001f1e7")
btn_lang_ru = KeyboardButton(text = "Русский \U0001f1f7\U0001f1fa")

keyboard = ReplyKeyboardMarkup(
    keyboard = [[btn_lang_en], [btn_lang_ru]],
    resize_keyboard = True
)

btn_beautify = InlineKeyboardButton(text = lang["EN"]["beautify"],
                                    callback_data = "beautify"
)
btn_analyze = InlineKeyboardButton(text = lang["EN"]["analyze"],
                                    callback_data = "analyze"
)
btn_get_info = InlineKeyboardButton(text = lang["EN"]["info"],
                                    callback_data = "info"
)
btn_reply = InlineKeyboardButton(text = lang["EN"]["reply"],
                                    callback_data = "reply"
)
btn_prop_sol = InlineKeyboardButton(text=lang["EN"]["solution"],
                                    callback_data = "solution"
)

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [[btn_beautify], [btn_analyze],
        [btn_get_info], [btn_reply], [btn_prop_sol]
    ]
)


@dp.message(CommandStart())
async def send_welcome(message : types.Message):
    
    await message.answer("Hello, choose the language:\nПривет, выберите язык:",
                        reply_markup = keyboard
    )


@dp.message(lambda message : message.text in ["English \U0001f1ec\U0001f1e7", "Русский \U0001f1f7\U0001f1fa"])
async def intro_message(message : types.Message):
    global use_language, main_keyboard
    
    if message.text == "English \U0001f1ec\U0001f1e7":
        use_language = "EN"
    else:
        use_language = "RU"
    
    btn_beautify = InlineKeyboardButton(text = lang[use_language]["beautify"],
                                        callback_data = "beautify"
    )
    btn_analyze = InlineKeyboardButton(text = lang[use_language]["analyze"],
                                        callback_data = "analyze"
    )
    btn_get_info = InlineKeyboardButton(text = lang[use_language]["info"],
                                        callback_data = "info"
    )
    btn_reply = InlineKeyboardButton(text = lang[use_language]["reply"],
                                        callback_data = "reply"
    )
    btn_prop_sol = InlineKeyboardButton(text=lang[use_language]["solution"],
                                        callback_data = "solution"
    )
    
    main_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [[btn_beautify], [btn_analyze],
            [btn_get_info], [btn_reply], [btn_prop_sol]
        ]
    )
    
    await message.answer(lang[use_language]["intro"])


async def ask_action(message : types.Message):
    await message.answer(
        message.text,
        reply_markup = main_keyboard
    )


@dp.message()
async def handle_user_text(message : types.Message):
    await ask_action(message)


@dp.callback_query()
async def handle_callback_query(callback_query: types.CallbackQuery):
    action = callback_query.data
    gpt = GenI()
    
    if action == "analyze":
        prompt = (lang[use_language]["prompt-analyze"] + 
            callback_query.message.text
        )
    elif action == "beautify":
        prompt = (lang[use_language]["prompt-beautify"] + 
            callback_query.message.text
        )
    elif action == "info":
        prompt = (lang[use_language]["prompt-info"] +
            callback_query.message.text
        )
    elif action == "solution":
        prompt = (lang[use_language]["prompt-solution"] +
            callback_query.message.text
        )
    else:
        prompt = (lang[use_language]["prompt-reply"] + 
            callback_query.message.text
        )
    
    answer = gpt.ask_gpt(prompt = prompt).replace("###", "•").replace("**", "")
    
    await callback_query.message.answer(answer)
    
    await callback_query.answer()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
