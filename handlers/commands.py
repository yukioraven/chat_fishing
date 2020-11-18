import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import CommandHandler

import engine_interface as ei
from localization import texter, tr, ul


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков команд")
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("language", language))
    dispatcher.add_handler(CommandHandler("start", start))


def help_command(update, context):
    logging.info("Получена команда \\language")
    user = update.effective_user
    chat = update.effective_chat
    u_data = context.user_data

    if chat.type == "private":
        ul(user, u_data)
        text = tr("help")
        user.send_message(text=text)


def language(update, context):
    logging.info("Получена команда \\language")
    user = update.effective_user
    chat = update.effective_chat
    u_data = context.user_data

    if chat.type == "private":
        ul(user, u_data)
        text = tr("choose_lang")
        markup = get_lang_markup(u_data)
        user.send_message(text=text, reply_markup=markup)


def start(update, context):
    logging.info("Получена команда \\start")
    user = update.effective_user
    chat = update.effective_chat
    u_data = context.user_data

    if chat.type == "private":
        if not ei.is_user_exist(u_data):
            ul(user, u_data)
            text = tr("setup_1")
            markup = get_lang_markup(u_data, after_start=True)
            user.send_message(text=text, reply_markup=markup)
        else:
            ul(user, u_data)
            text = tr("start_again")
            user.send_message(text=text)
    else:
        return


def get_lang_markup(user_data, after_start=False):
    keyboard = []
    for locale in texter.get_locales():
        if user_data["language"] != locale or after_start:
            callback_data = "lang#" + locale
            if after_start:
                callback_data += "#after_start"
            keyboard.append([InlineKeyboardButton(tr(locale), callback_data=callback_data)])
    return InlineKeyboardMarkup(keyboard)
