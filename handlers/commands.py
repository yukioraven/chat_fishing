import logging
from telegram import error
from telegram.ext import CommandHandler

import engine_interface as ei
from localization import tr, ul


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков команд")
    dispatcher.add_handler(CommandHandler("start", start))


def start(update, context):
    logging.info("Получена команда \\start")
    user = update.effective_user
    chat = update.effective_chat

    if chat.type == "private":
        text = ei.setup_user()
    elif chat.type == "group" or chat.type == "supergroup":
        user_status = chat.get_member(user.id).status
        if user_status == "creator" or user_status == "administrator":
            text = ei.setup_chat()
        else:
            text = tr("admins_only")
    else:
        return

    ul(update.effective_user, context.user_data)
    try:
        user.send_message(text=text)
    except error.Unauthorized:
        text = tr("unauthorized").format(user.name) + text
        chat.send_message(text=text)
