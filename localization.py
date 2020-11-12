import json
import logging
import os


class Texter(object):

    def __init__(self):
        self.locales = load_locales("locales")
        self.default_locale = "en"
        self.locale = self.default_locale

    def set_locale(self, locale):
        self.locale = locale

    def get_locales(self):
        return self.locales.keys()

    def get_text_for_label(self, label):
        if self.locale in self.locales and label in self.locales[self.locale]:
            return self.locales[self.locale][label]
        elif self.default_locale in self.locales and label in self.locales[self.default_locale]:
            logging.warning("Для локализации {} и метки {} отсутствует текст, "
                            "будет использован текст для локализации по умолчанию".format(self.locale, label))
            return self.locales[self.default_locale][label]
        else:
            logging.error("Для метки {} нет текста в локализации {} "
                          "и в локализации по умолчанию".format(label, self.locale))
            return "UNDEFINED"

    def update_locale(self, user, user_data):
        if "language" in user_data:
            locale = user_data["language"]
            logging.info("Будет использована сохраненная локализация: {}".format(locale))
            self.set_locale(locale)
            return
        elif hasattr(user, "language_code"):
            locale = locale_simplify(user.language_code)
            if locale in self.locales:
                logging.info("Нет сохраненной локализации, "
                             "будет сохранена и использована локализация из TG: {}".format(locale))
                user_data["language"] = locale
                self.set_locale(locale)
                return

        logging.warning("Локализация пользователя не указана или не поддержана, "
                        "будет использована локализация по умолчанию")
        user_data["language"] = self.default_locale
        self.set_locale(self.default_locale)


def load_locales(directory):
    result = {}
    for dirpath, unused, filenames in os.walk(directory):
        for filename in filenames:
            file = open(os.path.join(dirpath, filename), "r")
            json_data = file.read()
            data = json.loads(json_data)
            result[data["locale"]] = data["values"]
    return result


def locale_simplify(locale):
    if locale == "en-US" or locale == "en-GB":
        return "en"
    else:
        return locale


texter = Texter()
tr = texter.get_text_for_label
ul = texter.update_locale
