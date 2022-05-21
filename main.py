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

parent_path = Path(__file__).resolve().parent
updater = Updater("5377461148:AAFekpap_Fs-C-_3CVPi50nexYOsAQK-IuQ",
                  use_context=True)

keyboard = [
    [
        InlineKeyboardButton("Yes", callback_data="Yes"),
        InlineKeyboardButton("No", callback_data="No"),

    ]
]

ikm_yes_no = InlineKeyboardMarkup(keyboard)


def readfile_png(update: Update, context: CallbackContext):
    dc = update.message.photo[-1]
    ghazal = dc.get_file()
    path = parent_path.joinpath('junk/' + 'siavash.jpg')
    f_gcode = ghazal.download(str(path))

    text = ('done')
    update.message.reply_text(text)


PHOTO_PATH = 'junk/siavash.jpg'

bot = updater.bot

# bot.send_message(chat_id='-1567906020', text="From Telegram Bot")
#
# bot.send_photo(chat_id='-1567906020', photo=open(PHOTO_PATH, 'rb'),caption = 'hi')

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

ikm_full = InlineKeyboardMarkup(keyboard)

density_temp = ""
density_temp_float = ""
first_try = False
float_flag = False

density = 0.0


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")


def restart_set_density(chat_dict):
    chat_dict['density_temp'] = ""
    chat_dict['density_temp_float'] = ""
    chat_dict['first_try'] = True
    chat_dict['float_flag'] = False
    chat_dict['command'] = 'density'


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


def update_density(value=-1.0):
    global density
    if value != -1:
        density = value
        update_database('density', value)
    else:
        density = get_database('density')


def gcode(update: Update, context: CallbackContext):
    update.message.reply_text("Please upload your G_code : ")


def den(update: Update, context: CallbackContext):
    restart_set_density(context.chat_data)
    param_bot = update.message.text.replace('/set_density', '')

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    if param_bot == '':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="enter density",
                                 reply_markup=ikm_full)
    else:
        data = float(param_bot)
        update_density(data)
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


def button(update: Update, context: CallbackContext) -> None:
    if context.chat_data['command'] == 'density':
        density_button(update, context)
    elif context.chat_data['command'] == 'file_stl':
        density_button(update, context)


def density_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    chat_data = context.chat_data
    if chat_data['first_try']:
        chat_data['first_try'] = False

    if query.data == ".":
        chat_data['float_flag'] = True

    if query.data == "enter":
        data = float(chat_data['density_temp'] + "." + chat_data['density_temp_float'])
        update_density(data)
        query.edit_message_text(text=f"density set to {data}")
        context.chat_data['command'] = ''
        return

    if query.data.isdigit() and int(query.data) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        data = query.data

        if chat_data['float_flag']:
            chat_data['density_temp_float'] += data
        else:
            chat_data['density_temp'] += data

    if chat_data['float_flag']:
        density_1 = float(chat_data['density_temp'] + "." + chat_data['density_temp_float'])
    else:
        density_1 = chat_data['density_temp']

    query.answer()
    query.edit_message_text(text=f"density : {density_1}", reply_markup=ikm_full)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('upload_gcode', gcode))
updater.dispatcher.add_handler(CommandHandler('set_density', den))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(MessageHandler(Filters.document.file_extension('gcode'), readfile))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, readfile_png))

updater.start_polling()
