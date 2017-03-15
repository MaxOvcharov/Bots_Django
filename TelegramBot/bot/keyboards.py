# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from telebot import types


def markup_city_finder():
    """
        Generate keyboard - "City finder"
        :return: markup object
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, 
                                       one_time_keyboard=True,
                                       selective=True,
                                       row_width=1)
    # Create all buttons
    btn1 = types.KeyboardButton('Определить по Вашим геоданным', request_location=True)
    btn2 = types.KeyboardButton('Показать любой')
    markup.add(btn1, btn2)
    return markup


def markup_hider():
    markup = types.ReplyKeyboardRemove(True)
    return markup


def inline_go_to_city_url(city_name, city_url):
    markup = types.InlineKeyboardMarkup()
    city_url_button = types.InlineKeyboardButton(text="Перейти на страницу: {0}".
                                                 format(city_name), url=city_url)
    markup.add(city_url_button)
    return markup

