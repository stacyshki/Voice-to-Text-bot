from speech import SpeechProcessing
from text_processing import GenI
import asyncio
import logging
import json
from os import getenv, remove
from dotenv import load_dotenv
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardButton, InlineKeyboardMarkup
)


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


def set_inline_board(use_language : str = "EN"):
    '''
    Set a keyboard (buttons in the message)
    
    Args:
        use_language (str): set "EN" or "RU"
    '''
    
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
    btn_prop_sol = InlineKeyboardButton(text = lang[use_language]["solution"],
                                        callback_data = "solution"
    )
    btn_summarize = InlineKeyboardButton(text = lang[use_language]["summarize"],
                                        callback_data = "summarize"
    )
    btn_note = InlineKeyboardButton(text = lang[use_language]["note"],
                                        callback_data = "note"
    )
    btn_enhance = InlineKeyboardButton(text = lang[use_language]["enhancement"],
                                        callback_data = "enhancement"
    )
    
    main_keyboard = InlineKeyboardMarkup(
        inline_keyboard = [[btn_beautify], [btn_analyze],
            [btn_get_info], [btn_reply], [btn_prop_sol],
            [btn_note], [btn_summarize], [btn_enhance]
        ]
    )
    
    return main_keyboard


main_keyboard = set_inline_board()
use_language = "EN"


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
    
    main_keyboard = set_inline_board(use_language = use_language)
    
    await message.answer(lang[use_language]["intro"])


async def ask_action(message : types.Message):
    
    await message.answer(
        message.text,
        reply_markup = main_keyboard
    )


@dp.message(lambda message : message.text)
async def handle_user_text(message : types.Message):
    
    await ask_action(message)


@dp.callback_query()
async def handle_callback_query(callback_query : types.CallbackQuery):
    action = callback_query.data
    gpt = GenI()
    prompt = (lang[use_language]["prompt-" + action] + 
        callback_query.message.text
    )
    answer = gpt.ask_gpt(prompt = prompt).replace("###", "")
    
    await callback_query.message.answer(answer, parse_mode = "Markdown")
    
    await callback_query.answer()


@dp.message(lambda message : message.voice or message.audio or message.video or message.video_note)
async def handle_media_message(message : Message):
    """
    Handles voice messages, audio files, video files, and video notes.
    Downloads the file, transcribes it using SpeechProcessing, and sends back
    the transcribed text.
    The downloaded file is deleted after processing
    """
    
    if message.voice:
        file_id = message.voice.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.video_note:
        file_id = message.video_note.file_id
    else:
        return
    
    file = await bot.get_file(file_id)
    file_path = file.file_path
    local_filename = f"temp_{file_id}"
    
    await bot.download_file(file_path, local_filename)
    
    try:
        speech_processor = SpeechProcessing()
        transcribed_text = speech_processor.to_text(local_filename)
        
        await message.answer(transcribed_text, reply_markup = main_keyboard)
    finally:
        remove(local_filename)


async def main():
    
    await bot.delete_webhook(drop_pending_updates = True)
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
