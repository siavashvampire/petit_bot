from pathlib import Path

from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from MainCode import parent_path
from app.user.api import get_all_user, get_user, add_user
from core.api import download_photo
from core.config.database import channel_id
from app.idea.model import idea_model
from core.style.InlineKeyboardMarkup import ikm_yes_no

PHOTO_PATH = 'app/idea/junk/temp.jpg'


def restart_set_idea(chat_dict):
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
                                       text="process 2/10 [##----------]" + '\n' + \
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
                                       text="if there exist stl file ?",
                                       reply_markup=ikm_yes_no)
    chat_data['set_idea_send_message_id'] = message.message_id

    chat_data['command'] = 'set_idea_stl_file_Q'


def set_idea_same_innovator(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    chat_data = context.chat_data
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    if query.data == 'yes':
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 4/10 [####--------]" + '\n' + \
                                                "if there exist stl file ?",
                                           reply_markup=ikm_yes_no)

        chat_data['set_idea_innovator'] = chat_data['user_name']

        chat_data['set_idea_send_message_id'] = message.message_id

        chat_data['command'] = 'set_idea_stl_file_Q'
    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 3/10 [###--------]" + '\n' + \
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
                              chat_data['set_idea_description'], chat_data['overview'])
    overview = 'yes' if chat_data['overview'] else 'no'
    caption = chat_data['set_idea_description'] + '\n' + '#idea' + '\n' + 'innovator : ' + \
              chat_data['set_idea_innovator'] + '\n' + 'uploader : ' + chat_data['user_name'] + '\n' + 'overview : ' + \
              overview + '\n' + "idea_number :" + str(idea_id) + '\n' + 'file stl: ' + chat_data[
                  'file_question']

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
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 7/10 [#######-----]" + '\n' + \
                                                "your overview : ",
                                           reply_markup=ikm_yes_no)

        chat_data['set_idea_send_message_id'] = message.message_id

        chat_data['command'] = 'set_idea_set_overview'
    else:
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="process 5/10 [#####-------]" + '\n' + \
                                                "input your stl link,please : ")

        chat_data['set_idea_send_message_id'] = message.message_id
        chat_data['command'] = 'set_idea_input_stl_link'


def set_idea_input_stl_link(update: Update, context: CallbackContext):
    stl_link = update.message.text
    context.chat_data['set_idea_input_stl_link'] = stl_link
    chat_data = context.chat_data

    message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="process 6/10 [######------]" + '\n' + \
                                            "overview :",
                                       reply_markup=ikm_yes_no)

    chat_data['set_idea_send_message_id'] = message.message_id
    chat_data['command'] = 'set_idea_input_stl_file'


def set_idea(update: Update, context: CallbackContext) -> None:
    chat_data = context.chat_data
    user = get_user(username=update.effective_user.username)
    if not user.can_insert_idea():
        update.message.reply_text(text="you are not allowed to insert idea")
        return

    chat_data['command'] = 'set_idea_upload_picture'
    chat_data['user_name'] = '@' + user.username

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    message = context.bot.send_message(chat_id=update.effective_chat.id, text="process 0/10 [------------]" + '\n' + \
                                                                              "Please upload your picture as photos: ")
    chat_data['set_idea_send_message_id'] = message.message_id


def set_idea_upload_picture(update: Update, context: CallbackContext):
    chat_data = context.chat_data

    download_photo(update.message.photo[-1], 'app/idea/junk/' + 'temp.jpg')
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=chat_data['set_idea_send_message_id'])

    message = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="process 1/10 [#-----------]" + '\n' + \
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

    user.chang_idea_flag(True if query.data == 'yes' else False)

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    if query.data == 'yes':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="user " + user.username + " can set idea")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="user " + user.username + " can not set idea")

    restart_set_idea(chat_data)
    query.answer()
