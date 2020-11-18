import logging
from telegram import InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler

import engine_interface as ei
from localization import tr, ul


def init_handlers(dispatcher):
    logging.info("Инициализация обработчиков кнопок")
    dispatcher.add_handler(CallbackQueryHandler(button))


def button(update, context):
    query = update.callback_query
    query.answer()
    user = update.effective_user
    u_data = context.user_data
    logging.info("Нажата кнопка, информация о нажатии: %s", query.data)
    data_list = query.data.split("#")
    if data_list[0] == "lang":
        u_data["language"] = data_list[1]
        ul(user, u_data)
        text = tr("lang_set")
        if len(data_list) > 2 and data_list[2] == "after_start":
            ei.create_user(u_data)
            text += tr("start")
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        user.send_message(text=text)
