from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from app.accounting.main import set_accounting_upload_picture, set_accounting_upload_pdf_file
from app.density.main import density_set_density
from app.idea.main import idea_stl_file_question, set_idea_accepted_idea, set_idea_same_innovator, \
    set_idea_input_description, set_idea_input_innovator, set_idea_upload_picture, set_idea_change_user_idea_start, \
    set_idea_change_user_idea, set_idea_input_stl_link, set_idea_insert_stl_file, set_idea_overview, \
    set_idea_insert_idea


def button(update: Update, context: CallbackContext) -> None:
    if context.chat_data['command'] == 'density':
        density_set_density(update, context)
    elif context.chat_data['command'] == 'set_idea_stl_file_Q':
        idea_stl_file_question(update, context)
    elif context.chat_data['command'] == 'set_idea_set_overview':
        set_idea_accepted_idea(update, context)
    elif context.chat_data['command'] == 'set_idea_same_innovator':
        set_idea_same_innovator(update, context)
    elif context.chat_data['command'] == 'set_idea_change_user_idea':
        set_idea_change_user_idea(update, context)
    elif context.chat_data['command'] == 'set_idea_insert_stl_file':
        set_idea_insert_stl_file(update, context)





def input_text(update: Update, context: CallbackContext) -> None:
    chat_data = context.chat_data
    if 'command' not in chat_data.keys() or chat_data['command'] == '':
        update.message.reply_text("command not set")
        return
    elif chat_data['command'] == 'set_idea_input_description':
        set_idea_input_description(update, context)
    elif chat_data['command'] == 'set_idea_input_innovator':
        set_idea_input_innovator(update, context)
    elif chat_data['command'] == 'set_idea_change_user_idea_start':
        set_idea_change_user_idea_start(update, context)
    elif context.chat_data['command'] == 'set_idea_input_stl_link':
        set_idea_input_stl_link(update, context)
    elif context.chat_data['command'] == 'set_idea_overview':
        set_idea_overview(update, context)



def readfile_png(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    if 'command' not in chat_data.keys() or chat_data['command'] == '':
        update.message.reply_text("command not set")
        return
    elif chat_data['command'] == 'set_idea_upload_picture':
        set_idea_upload_picture(update, context)

    elif chat_data['command'] == 'set_accounting_upload':
        set_accounting_upload_picture(update, context)
    else:
        update.message.reply_text("command that set is wrong")
        return


def pdf_handler(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    if 'command' not in chat_data.keys() or chat_data['command'] == '':
        update.message.reply_text("command not set")
        return
    elif chat_data['command'] == 'set_accounting_upload':
        set_accounting_upload_pdf_file(update, context)
    else:
        update.message.reply_text("command that set is wrong")
        return
