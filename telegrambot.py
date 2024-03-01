import telebot
import dbadapter
from subscription import Subscription
from util import timestamp
import os
from dotenv import load_dotenv

def create_subscription(message):
    chat_id = message.from_user.id
    full_name = message.from_user.full_name
    return Subscription(full_name, chat_id, True, timestamp())

def already_exists(subscription):
    for sub in dbadapter.get_all_subscriptions():
        if str(subscription.chat_id) == sub.chat_id:
            return True
    return False

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_API'))
print("Bot started...")

@bot.message_handler(commands=['start'])
def send_terms(message):
    terms = dbadapter.get_all_terms()
    if(len(terms) == 0):
        reply = "Trenutno nema termina u lokalnoj bazi!"
    else:
        reply = "Termini u lokalnoj bazi:"
    for term in terms:
        if term.is_available:
            reply += "\n"
            reply += term.fancyprint()
    bot.reply_to(message, reply)


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    sub = create_subscription(message)
    if already_exists(sub):
        sub.enable()
        dbadapter.update_subscription(sub)
    else:
        dbadapter.insert_subscription(sub)
    bot.reply_to(message, "Uspesno prijavljen na obavestenja!")

@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    sub = create_subscription(message)
    sub.disable()
    dbadapter.update_subscription(sub)
    bot.reply_to(message, "Uspesno odjavljen sa obavestenja!")


@bot.message_handler(commands=['id'])
def send_id(message):
    bot.reply_to(message, message.chat.id)

bot.infinity_polling()

