import os

import telebot
import random
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from words import words
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)


user_xp = {}
current_question = {}


#START_MENU
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.add(
        KeyboardButton("📚 Words"),
        KeyboardButton("🧠 My progress")
   )

    bot.send_message(
        message.chat.id,
        "🇩🇪 Welcome to Deutch_Learn Bot!\nChoose action:",
        reply_markup=keyboard
    )


#LESSON
@bot.message_handler(func=lambda m: m.text == "📚 Words")
def lesson(message):
    word = random.choice(words)
    current_question[message.chat.id] = word

    bot.send_message(
        message.chat.id,
        f"🇩🇪🇷🇺 Translate the word: {word['de']}"
    )


#CHECK_ANSWER
@bot.message_handler(func=lambda m: m.text not in ["📚 Words", "🧠 My progress"])
def check_answer(message):
    chat_id = message.chat.id

    if chat_id not in current_question:
        return

    word = current_question[chat_id]
    correct = word["ru"]

    if message.text.lower().strip() == correct.lower():
        bot.send_message(chat_id, "✅ Great! +10 XP")

        user_xp[chat_id] = user_xp.get(chat_id, 0) + 10
        del current_question[chat_id]

    else:
        bot.send_message(
            chat_id,
            f"❌ Incorrect.\nCorrect answer: {correct}"
        )


#PROGRESS
@bot.message_handler(func=lambda m: m.text == "🧠 My progress")
def progress(message):
    xp = user_xp.get(message.chat.id, 0)

    bot.send_message(
        message.chat.id,
        f"📊 Your XP: {xp}"
    )


#RUN
bot.infinity_polling()


