# from telegram.ext.updater import Updater
# from telegram.update import Update
# from pathlib import Path
# import telegram
# from telegram.ext.filters import Filters
# from telegram.ext.callbackcontext import CallbackContext
# from telegram.ext.commandhandler import CommandHandler
# from telegram.ext.messagehandler import MessageHandler
#
# parent_path = Path(__file__).resolve().parent
# updater = Updater("5377461148:AAFekpap_Fs-C-_3CVPi50nexYOsAQK-IuQ",
#                   use_context=True)
#
# TELEGRAM_BOT_TOKEN=('5377461148:AAFekpap_Fs-C-_3CVPi50nexYOsAQK-IuQ')
#
# def readfile(update: Update, context: CallbackContext):
#     dc = update.message.photo[-1]
#     ghazal = dc.get_file()
#     path = parent_path.joinpath('junk/' + 'siavash.jpg')
#     f_gcode = ghazal.download(str(path))
#
#
#
#     text = ('done')
#     update.message.reply_text(text)
#
#
# def gcode(update: Update, context: CallbackContext):
#     update.message.reply_text("Please upload your G_code : ")
#
# TELEGRAM_CHAT_ID = '-1001306...'
# PHOTO_PATH = 'junk/siavash.jpg'
#
# bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
#
# bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="From Telegram Bot")
#
# bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(PHOTO_PATH, 'rb'))
#
#
# updater.dispatcher.add_handler(CommandHandler('upload_gcode', gcode))
# # updater.dispatcher.add_handler(MessageHandler(Filters.document.file_extension('gcode'), readfile))

# updater.dispatcher.add_handler(MessageHandler(Filters.photo, readfile))
#
# updater.start_polling()

asd_list = []

from database_poll import *

get_database_by_step(1)


print(asd_list)
