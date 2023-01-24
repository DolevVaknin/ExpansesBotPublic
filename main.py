import telebot
import datetime
import csv

bot = telebot.TeleBot("5869585883:AAFQYQ4rXwDd5BcYC-bsIZpCoefRBwM54Uw")
date = datetime.date.today()
amount = ""
waster = ""
description = ""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def first_message(message):
    bot.reply_to(message, "Hello\nPlease choose a day:\n1. Today\n2. Yesterday\n3. The day before yesterday")
    bot.register_next_step_handler(message, date_message)

@bot.message_handler(func=lambda message: True)
def date_message(message):
    global date
    if(message.text == "1"):
        date = datetime.date.today()
    if(message.text == "2"):
        date = datetime.date.today() - datetime.timedelta(days=1)
    if(message.text == "3"):
        date = datetime.date.today() - datetime.timedelta(days=2)
    bot.reply_to(message, "Amount:\n")
    bot.register_next_step_handler(message, amount_message)

@bot.message_handler(func=lambda message: True)
def amount_message(message):
    global amount
    amount = message.text
    bot.reply_to(message, "Wasted by:\n1. Dolev\n2. Marina\n3. Other")
    bot.register_next_step_handler(message, waster_message)

@bot.message_handler(func=lambda message: True)
def waster_message(message):
    global waster
    if (message.text == "1"):
        waster = "Dolev"
    if (message.text == "2"):
        waster = "Marina"
    if (message.text == "3"):
        waster = "Other"

    if(waster == "Other"):
        bot.reply_to(message, "Please add a description:\n")
        bot.register_next_step_handler(message, description_message)
    else:
        bot.reply_to(message, "Thanks! The Expanse was added.\n")
        with open("Expanses.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date.strftime("%d/%m/%Y"), amount, waster, description])


@bot.message_handler(func=lambda message: True)
def description_message(message):
    global description
    description = message.text
    with open("Expanses.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date.strftime("%d/%m/%Y"), amount, waster, description])
    bot.reply_to(message, "Thanks! The Expanse was added.\n")


bot.polling()
