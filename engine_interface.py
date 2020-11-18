import logging


def is_user_exist(user_data):
    return "mastery" in user_data


def create_user(user_data):
    user_data["mastery"] = 0
