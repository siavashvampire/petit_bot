from pathlib import Path
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from app.user.api import add_user

parent_path = Path(__file__).resolve().parent


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.")
    add_user(update.message.from_user)


if __name__ == '__main__':
    from telegram.ext import CallbackQueryHandler
    from telegram.ext.updater import Updater
    from telegram.ext.commandhandler import CommandHandler
    from telegram.ext.messagehandler import MessageHandler
    from telegram.ext.filters import Filters
    from app.density.main import den
    from app.gcode.main import gcode, readfile
    from app.idea.main import set_idea, add_user_idea
    from core.config.database import telegram_token
    from core.handler import button, readfile_png, input_text, pdf_handler
    from app.accounting.main import set_accounting

    updater = Updater(telegram_token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('upload_gcode', gcode))
    updater.dispatcher.add_handler(CommandHandler('set_density', den))
    updater.dispatcher.add_handler(CommandHandler('set_idea', set_idea))
    updater.dispatcher.add_handler(CommandHandler('set_accounting', set_accounting))
    updater.dispatcher.add_handler(CommandHandler('add_user_idea', add_user_idea))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(MessageHandler(Filters.document.file_extension('gcode'), readfile))
    updater.dispatcher.add_handler(MessageHandler(Filters.document.pdf, pdf_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, readfile_png))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, input_text))

    print('bot is running')
    updater.start_polling()
