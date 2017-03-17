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


def inline_go_to_city_url(city_name=None, city_url=None):
    markup = types.InlineKeyboardMarkup()
    city_url_button = types.InlineKeyboardButton(text="Перейти на страницу города: {0}".
                                                 format(city_name), url=city_url)
    markup.add(city_url_button)
    return markup


def inline_city_vote(like=False, like_num=0, city_name=""):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if like:
        like_button = types.InlineKeyboardButton(text=u"\u2764 {0}".format(like_num + 1),
                                                 callback_data="like_{0}".format(city_name))
    else:
        like_button = types.InlineKeyboardButton(text=u"\u2764 {0}".format(like_num),
                                                 callback_data="like_{0}".format(city_name))
    markup.add(like_button)
    return markup

