from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from app.density.database.database import update_density_db
from core.style.InlineKeyboardMarkup import ikm_full


def den(update: Update, context: CallbackContext) -> None:
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


def restart_set_density(chat_dict):
    chat_dict['density_temp'] = ""
    chat_dict['density_temp_float'] = ""
    chat_dict['first_try'] = True
    chat_dict['float_flag'] = False
    chat_dict['command'] = 'density'


def update_density(value: float = -1.0) -> None:
    update_density_db(value)
