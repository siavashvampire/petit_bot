# from app.user.api import get_user

# UserDB.is_idea_admin()
# # asd = get_user(id=72025606)
# from pathlib import Path
# from telegram.update import Update
# from telegram.ext.callbackcontext import CallbackContext
#
# parent_path = Path(__file__).resolve().parent
#
#
# def set_idea_input_stl_file(update: Update, context: CallbackContext):
#     file = update.message.document
#     newFile = file.getFile()
#     newFile.download('stl')
#     path = parent_path.joinpath('app/idea/junk/' + file.fil_name)
#
#     chat_data = context.chat_data
#
#     message = context.bot.send_message(chat_id=update.effective_chat.id,
#                                        text="process 8/10 [########--]" + '\n' + \
#                                             "overview :")
#
#     path = parent_path.joinpath(newFile)
#
#     chat_data['set_idea_send_message_id'] = message.message_id
#     chat_data['command'] = 'unknown'

def set_idea_input_stl_link(update: Update, context: CallbackContext):
    stl_link = update.message.text
    context.chat_data['set_idea_input_stl_link'] = stl_link
    chat_data = context.chat_data
    query = update.callback_query
    query.answer()

    if query.data=='yes':

        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="process 6/10 [######------]" + '\n' + \
                                            "if there exist stl_file ? :",
                                       reply_markup=ikm_yes_no)
        chat_data['set_idea_send_message_id'] = message.message_id
        chat_data['command'] = 'set_idea_input_stl_file'
    else :
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="process 6/10 [######------]" + '\n' + \
                                            "Overview :")



        chat_data['set_idea_send_message_id'] = message.message_id
        chat_data['command'] = 'set_idea_overview'


def set_idea_insert_stl_file(update: Update, context: CallbackContext):
    chat_data = context.chat_data

    download_file(update.message.file[0], 'app/idea/junk/stl_file')
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=chat_data['set_idea_send_message_id'])

    message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="process 1/10 [#-----------]" + '\n' + \
                                            "Overview :")

    chat_data['set_idea_send_message_id'] = message.message_id

    chat_data['command'] = 'set_idea_overview'

def set_idea_overview (update: Update, context: CallbackContext) :
    overview = update.message.text
    if:

    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=('Process finished'))

        chat_data['set_idea_send_message_id'] = message.message_id