from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from pathlib import Path
from database import update_database, get_database

density = get_database('density')
parent_path = Path(__file__).resolve().parent

updater = Updater("5377461148:AAFekpap_Fs-C-_3CVPi50nexYOsAQK-IuQ",
                  use_context=True)

keyboard = [
    [
        InlineKeyboardButton("7", callback_data="7"),
        InlineKeyboardButton("8", callback_data="8"),
        InlineKeyboardButton("9", callback_data="9"),
    ],
    [
        InlineKeyboardButton("4", callback_data="4"),
        InlineKeyboardButton("5", callback_data="5"),
        InlineKeyboardButton("6", callback_data="6"),
    ],
    [
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
        InlineKeyboardButton("3", callback_data="3"),
    ],
    [
        InlineKeyboardButton(".", callback_data="."),
        InlineKeyboardButton("0", callback_data="0"),
        InlineKeyboardButton("Enter", callback_data="enter"),
    ],
]

inline_keyboard_markup = InlineKeyboardMarkup(keyboard)

density_temp = ""
density_temp_float = ""
first_try = False
float_flag = False


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("qwdsa")


def read_float_number(data: str, text: str) -> float:
    import re
    re_value: list = re.findall(text + "\d+\.\d+", data)
    if len(re_value) == 0:
        return 0
    else:
        re_value: str = re_value[0]

    return float(re.findall("\d+\.\d+", re_value)[0])


def read_int_number(data: str, text: str) -> int:
    import re
    re_value: list = re.findall(text + "\d+", data)
    if len(re_value) == 0:
        return 0
    else:
        re_value: str = re_value[0]
    return int(re.findall("\d+", re_value)[0])


def gcode(update: Update, context: CallbackContext):
    update.message.reply_text("Please upload your G_code : ")


def den(update: Update, context: CallbackContext):
    global first_try, density
    first_try = True
    param_bot = update.message.text.replace('/set_density', '')

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    if param_bot == '':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="enter density",
                                 reply_markup=inline_keyboard_markup)
    else:
        data = float(param_bot)
        density = data
        update_database('density', data)
        update.message.reply_text(text=f"density set to {data}")


def readfile(update: Update, context: CallbackContext):
    dc = update.message.document
    ghazal = dc.get_file()
    path = parent_path.joinpath('junk/' + dc.file_name)
    f_gcode = ghazal.download(str(path))
    path = path.joinpath(f_gcode)

    # print(path)
    with open(path, 'r') as f_gcode:
        data = f_gcode.read()
    Path.unlink(path)
    time = read_int_number(data, "TIME:")
    minute = time // 60
    hour = minute // 60
    minute = minute % 60
    seconds = time % 60

    filament = read_float_number(data, "Filament used: ")
    x_min = read_float_number(data, "MINX:")
    y_min = read_float_number(data, "MINY:")
    z_min = read_float_number(data, "MINZ:")
    x_max = read_float_number(data, "MAXX:")
    y_max = read_float_number(data, "MAXY:")
    z_max = read_float_number(data, "MAXZ:")

    x = round(x_max - x_min, 1)
    y = round(y_max - y_min, 1)
    z = round(z_max - z_min, 1)
    d = round(density * filament)

    text = "time = "

    if hour != 0:
        text += str(hour) + " hour" + " and "

    if minute != 0:
        text += str(minute) + " minutes" + " and "

    text += str(seconds) + " seconds " + "\n"

    text += "filamnt used = " + str(filament) + " m" + "\n" + \
            "x_dimention = " + str(x) + "\n" + \
            "y_dimension = " + str(y) + "\n" + \
            "z_dimension = " + str(z) + "\n" + \
            "weight = " + str(d) + " gram"
    update.message.reply_text(text)

    # text_1 = "Density = " + str(d) + " gram"
    # update.message.reply_text(text_1)


def button(update: Update, context) -> None:
    query = update.callback_query
    global first_try, density_temp, density_temp_float, float_flag, density
    if first_try:
        first_try = False
        density_temp = ""
        density_temp_float = ""
        float_flag = False

    if query.data == ".":
        float_flag = True

    if query.data == "enter":
        data = float(density_temp + "." + density_temp_float)
        density = data
        update_database('density', data)
        query.edit_message_text(text=f"density set to {data}")
        return

    if query.data.isdigit() and int(query.data) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        data = query.data

        if float_flag:
            # density_temp_float *= 10
            density_temp_float += data
        else:
            # density_temp *= 10
            density_temp += data

    if float_flag:
        density_1 = float(density_temp + "." + density_temp_float)
    else:
        density_1 = density_temp

    query.answer()
    query.edit_message_text(text=f"density : {density_1}", reply_markup=inline_keyboard_markup)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('upload_gcode', gcode))
updater.dispatcher.add_handler(CommandHandler('set_density', den))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(MessageHandler(Filters.document.file_extension('gcode'), readfile))

updater.start_polling()
