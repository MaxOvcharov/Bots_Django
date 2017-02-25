# -*- coding: utf-8 -*-

from telebot import types


def markup_city_finder():
    """
        Generate keyboard - "City finder"
        :return: markup object
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Create all buttons
    #markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Вести название города')
    btn2 = types.KeyboardButton('Определить по Вашим геоданным')
    btn3 = types.KeyboardButton('Показать случайный...?!')
    markup.add(btn1, btn2, btn3)

    return markup
