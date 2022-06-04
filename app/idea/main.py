import validators
from pathlib import Path

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from MainCode import parent_path
from app.user.api import get_all_user, get_user
from core.api import download_photo, download_document, format_url
from core.config.database import channel_id
from app.idea.model import idea_model
from core.style.InlineKeyboardMarkup import ikm_yes_no

PHOTO_PATH = 'app/idea/junk/temp.jpg'


def restart_set_idea(chat_dict: dict):
    chat_dict.pop('command', "")
    chat_dict.pop('user_name', "")
    chat_dict.pop('set_idea_send_message_id', "")
    chat_dict.pop('set_idea_description', "")
    chat_dict.pop('set_idea_innovator', "")
    chat_dict.pop('file_question', "")
    chat_dict.pop('overview', "")
    chat_dict.pop('value', "")
    path = parent_path.joinpath(PHOTO_PATH)
    Path.unlink(path, missing_ok=True)


def set_idea_input_description(update: Update, context: CallbackContext) -> None:
    chat_data = context.chat_data
    chat_data['set_idea_description'] = update.message.text
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=chat_data['set_idea_send_message_id'])

    message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="process 3/11 [###--------]" + '\n' + \
                                            "same person as uploader?",
                                       reply_markup=ikm_yes_no)

    chat_data['set_idea_send_message_id'] = message.message_id

    chat_data['command'] = 'set_idea_same_innovator'


def set_idea_input_innovator(update: Update, context: CallbackContext) -> None:
    chat_data = context.chat_data
    chat_data['set_idea_innovator'] = update.message.text
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=chat_data['set_idea_send_message_id'])

    message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="process 5/11 [#####------]" + '\n' + \
                                            "if there exist stl file ?",
                                       reply_markup=ikm_yes_no)
    chat_data['set_idea_send_message_id'] = message.message_id

    chat_data['command'] = 'set_idea_stl_file_Q'


def set_idea_same_innovator(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    chat_data = context.chat_data
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    if query.data == 'yes':
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 6/11 [######-------]" + '\n' + \
                                                "if there exist stl file ?",
                                           reply_markup=ikm_yes_no)

        chat_data['set_idea_innovator'] = chat_data['user_name']

        chat_data['set_idea_send_message_id'] = message.message_id

        chat_data['command'] = 'set_idea_stl_file_Q'
    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 4/11 [####--------]" + '\n' + \
                                                "Please send innovator for this idea :"
                                           )
        chat_data['set_idea_send_message_id'] = message.message_id

        chat_data['command'] = 'set_idea_input_innovator'

    query.answer()


def set_idea_accepted_idea(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    chat_data = context.chat_data
    chat_data['overview'] = True if query.data == 'yes' else False

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    set_idea_insert_idea(update, context)

    query.answer()


def set_idea_insert_idea(update: Update, context: CallbackContext) -> None:
    chat_data = context.chat_data
    idea_id = idea_model.Idea(chat_data['user_name'], chat_data['set_idea_innovator'],
                              chat_data['set_idea_description'], chat_data['overview']).insert_idea()
    overview = chat_data['overview'] if 'overview' in chat_data and chat_data['overview'] else 'Not decided yet !'
    stl_link = 'yes : ' + chat_data['stl_link'] if chat_data['stl_link'] else 'Not existed ! '
    # stl_file = 'yes' if chat_data['set_idea_upload_stl_file'] else 'Not existed ! '

    caption = chat_data['set_idea_description'] + '\n' + '#idea' + '\n' + 'innovator : ' + \
              chat_data['set_idea_innovator'] + '\n' + 'uploader : ' + chat_data['user_name'] + '\n' + 'overview : ' + \
              overview + '\n' + "idea_number :" + str(idea_id) + '\n' + 'file stl: ' + chat_data[
                  'file_question'] + '\n' + 'stl_link :' + stl_link

    message_temp = context.bot.send_message(chat_id=update.effective_chat.id, text="start uploading and posting idea")

    message = context.bot.send_photo(chat_id=channel_id, photo=open(PHOTO_PATH, 'rb'), caption=caption)

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_temp.message_id)
    message_temp = context.bot.send_message(chat_id=update.effective_chat.id, text="forwarding the post")

    context.bot.forwardMessage(chat_id=update.effective_chat.id, from_chat_id=channel_id, message_id=message.message_id)

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_temp.message_id)

    restart_set_idea(chat_data)


def idea_stl_file_question(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    chat_data = context.chat_data
    chat_data['file_question'] = query.data

    if query.data == 'no':
        user = get_user(user=update.effective_user)
        if user.is_idea_admin():
            message = context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="process 11/11 [###########]" + '\n' + \
                                                    "your overview :")

            chat_data['set_idea_send_message_id'] = message.message_id
            chat_data['command'] = 'set_idea_overview'

        else:
            message = context.bot.send_message(chat_id=update.effective_chat.id,
                                               text="process 11/11 [###########]" + '\n' + \
                                                    "you're almost done ! ")
            set_idea_insert_idea(update, context)

        chat_data['set_idea_send_message_id'] = message.message_id

        chat_data['command'] = 'set_idea_insert_idea'
    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 7/11 [#######----]" + '\n' + \
                                                "insert your stl link,please : ")
        #
        # context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
        # context.bot.delete_message(chat_id=update.effective_chat.id, message_id=chat_data['set_idea_send_message_id'])

        chat_data['set_idea_send_message_id'] = message.message_id
        chat_data['command'] = 'set_idea_input_stl_link'


def set_idea_input_stl_link(update: Update, context: CallbackContext):
    stl_link = update.message.text
    context.chat_data['set_idea_input_stl_link'] = stl_link
    chat_data = context.chat_data

    val: bool = validators.url(format_url(stl_link))

    if val:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 8/11 [########---]" + '\n' + \
                                                "if there exist stl_file ? :",
                                           reply_markup=ikm_yes_no)

        chat_data['stl_link'] = stl_link
        chat_data['set_idea_send_message_id'] = message.message_id
        chat_data['command'] = 'set_idea_insert_stl_file'

    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 7/11 [########---]" + '\n' + \
                                                "Invalid link , please insert again :")

        chat_data['set_idea_send_message_id'] = message.message_id
        chat_data['command'] = 'set_idea_insert_stl_file'


def set_idea_insert_stl_file(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    query = update.callback_query
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    # context.bot.delete_message(chat_id=update.effective_chat.id, message_id=chat_data['set_idea_send_message_id'])

    if query.data == 'yes':
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 9/11 [#########--]" + '\n' + \
                                                "upload your stl file,please ")

        chat_data['set_idea_send_message_id'] = message.message_id

        chat_data['command'] = 'set_idea_upload_stl_file'
    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 4/11 [####-------]" + '\n' + \
                                                " process almost done ! :")

        chat_data['set_idea_send_message_id'] = message.message_id

        chat_data['command'] = 'set_idea_overview'

    query.answer()
    set_idea_insert_idea(update, context)

    # download_document(update.message.file[0], 'app/idea/junk/stl_file')


def set_idea_upload_stl_file(update: Update, context: CallbackContext):
    chat_data = context.chat_data

    download_document(update.message.document, 'app/idea/junk/stl_file/')
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=chat_data['set_idea_send_message_id'])
    user = get_user(user=update.effective_user)
    if user.is_idea_admin():
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 11/11 [###########]" + '\n' + \
                                                "your overview :")

        chat_data['set_idea_send_message_id'] = message.message_id
        chat_data['command'] = 'set_idea_overview'

    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Process finished!')

        chat_data['set_idea_send_message_id'] = message.message_id
        chat_data['command'] = 'set_idea_insert_idea'
        set_idea_insert_idea(update, context)


def set_idea_overview(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    chat_data['overview'] = update.message.text

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    user = get_user(user=update.effective_user)
    if user.is_idea_admin():
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 11/11 [###########]" + '\n' + \
                                                "your overview :")

        chat_data['set_idea_send_message_id'] = message.message_id

        chat_data['command'] = 'set_idea_insert_idea'

    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=('Process finished!'))

        chat_data['set_idea_send_message_id'] = message.message_id
        chat_data['command'] = 'set_idea_insert_idea'
        set_idea_insert_idea(update, context)


def set_idea(update: Update, context: CallbackContext) -> None:
    chat_data = context.chat_data
    user = get_user(username=update.effective_user.username)
    if not user.can_insert_idea():
        update.message.reply_text(text="you are not allowed to insert idea")
        return

    chat_data['command'] = 'set_idea_upload_picture'
    chat_data['user_name'] = '@' + user.username

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    message = context.bot.send_message(chat_id=update.effective_chat.id, text="process 1/10 [#----------]" + '\n' + \
                                                                              "Please upload your picture as photos: ")
    chat_data['set_idea_send_message_id'] = message.message_id


def set_idea_upload_picture(update: Update, context: CallbackContext):
    chat_data = context.chat_data

    download_photo(update.message.photo[-1], 'app/idea/junk/' + 'temp.jpg')
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=chat_data['set_idea_send_message_id'])

    message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="process 2/11 [##---------]" + '\n' + \
                                            "Please send description for this idea :")

    chat_data['set_idea_send_message_id'] = message.message_id

    chat_data['command'] = 'set_idea_input_description'


def add_user_idea(update: Update, context: CallbackContext):
    user = get_user(user=update.effective_user)
    chat_data = context.chat_data
    if not user.is_idea_admin():
        update.message.reply_text(text="you are not allowed")
        return

    keyboard = []
    users = get_all_user()

    for i in users:
        if i.username:
            keyboard.append([KeyboardButton(i.username, resize_keyboard=True)])

    ikm_idea_user = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="choose your user who you want change",
                                       reply_markup=ikm_idea_user)
    chat_data['set_idea_send_message_id'] = message.message_id
    context.chat_data['command'] = 'set_idea_change_user_idea_start'


def set_idea_change_user_idea_start(update: Update, context: CallbackContext):
    user = update.message.text
    chat_data = context.chat_data

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=chat_data['set_idea_send_message_id'])
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=user + " admin beshe ya na??",
                                       reply_markup=ikm_yes_no)
    chat_data['set_idea_send_message_id'] = message.message_id

    chat_data['command'] = 'set_idea_change_user_idea'
    chat_data['value'] = user


def set_idea_change_user_idea(update: Update, context: CallbackContext):
    query = update.callback_query

    chat_data = context.chat_data
    user = get_user(username=chat_data['value'])

    user.change_idea_flag(True if query.data == 'yes' else False)

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    if query.data == 'yes':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="user " + user.username + " can set idea")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="user " + user.username + " can not set idea")

    restart_set_idea(chat_data)
    query.answer()
