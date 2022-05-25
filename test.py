# from app.user.api import get_user

# UserDB.is_idea_admin()
# asd = get_user(id=72025606)
from pathlib import Path
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

parent_path = Path(__file__).resolve().parent


def set_idea_input_stl_file(update: Update, context: CallbackContext):
    file = update.message.document
    newFile = file.getFile()
    newFile.download('stl')
    path = parent_path.joinpath('app/idea/junk/' + file.fil_name)

    chat_data = context.chat_data

    message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="process 8/10 [########--]" + '\n' + \
                                            "overview :")

    path = parent_path.joinpath(newFile)

    chat_data['set_idea_send_message_id'] = message.message_id
    chat_data['command'] = 'unknown'
