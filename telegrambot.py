import telebot
import dbadapter
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_API'))
print("Bot started...")

@bot.message_handler(commands=['start', 'termini'])
def send_terms(message):
    terms = dbadapter.get_all()
    if(len(terms) == 0):
        reply = "Trenutno nema termina u lokalnoj bazi!"
    else:
        reply = "Termini u lokalnoj bazi:"
    for term in terms:
        if term.is_available:
            reply += "\n"
            reply += term.fancyprint()
    bot.reply_to(message, reply)

@bot.message_handler(commands=['id'])
def send_id(message):
    bot.reply_to(message, message.chat.id)

bot.infinity_polling()