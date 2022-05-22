from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from pathlib import Path
from database_poll import *

parent_path = Path(__file__).resolve().parent

updater = Updater("5377461148:AAFekpap_Fs-C-_3CVPi50nexYOsAQK-IuQ",
                  use_context=True)

keyboard = [
    [
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
        InlineKeyboardButton("3", callback_data="3"),
    ],
    [
        InlineKeyboardButton("4", callback_data="4"),
        InlineKeyboardButton("5", callback_data="5"),
    ],
]

inline_keyboard_markup = InlineKeyboardMarkup(keyboard)

N_pic = 6


def den(update: Update, context: CallbackContext):
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Picture Number : 1",
                             reply_markup=inline_keyboard_markup)


def button(update: Update, context) -> None:
    query = update.callback_query
    id = update.effective_chat.id

    asd = get_database_step_by_id(id)

    if asd:
        step = get_database_step_by_id(id) + 1
    else:
        step = 1
        # insert_database(id, step, 0)

    if query.data.isdigit() and int(query.data) in [1, 2, 3, 4, 5]:
        data = int(query.data)
        insert_database(id, step, data)

    if step == N_pic:
        query.edit_message_text(text=f"poll is done")
        return

    query.answer()
    query.edit_message_text(text=f"Picture Number : {step + 1}", reply_markup=inline_keyboard_markup)


def result(update: Update, context: CallbackContext):
    text_all = ""
    for i in range(N_pic):
        asd = get_database_mean_by_step(i + 1)
        text = "Picture " + str(i + 1) + " : " + str(asd) + "\n"
        text_all += text

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text_all)


def myFunc(e):
    return e['value']


def result_sort(update: Update, context: CallbackContext):
    asd_list = []
    for i in range(N_pic):
        asd = get_database_mean_by_step(i + 1)
        temp = {}
        temp['id'] = i + 1
        temp['value'] = asd
        asd_list.append(temp)

    asd_list.sort(key=myFunc, reverse=True)
    text_all = ""
    for i in asd_list:
        text = "Picture " + str(i['id']) + " : " + str(i['value']) + "\n"
        text_all += text

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text_all)

def delete_poll(update: Update, context: CallbackContext):
    delete_database_by_id(update.effective_chat.id)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="data deleted")


updater.dispatcher.add_handler(CommandHandler('bot_poll', den))
updater.dispatcher.add_handler(CommandHandler('result', result))
updater.dispatcher.add_handler(CommandHandler('result_sort', result_sort))
updater.dispatcher.add_handler(CommandHandler('delete_poll', delete_poll))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
