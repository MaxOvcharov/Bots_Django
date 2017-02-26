# -*- coding: utf-8 -*-

from telebot import types
from models import Cities, CityPhotos


def markup_city_finder():
    """
        Generate keyboard - "City finder"
        :return: markup object
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True,
                                       row_width=1)
    # Create all buttons
    btn1 = types.KeyboardButton('Ввести название города')
    btn2 = types.KeyboardButton('Определить по Вашим геоданным')
    btn3 = types.KeyboardButton('Показать случайный')
    markup.add(btn1, btn2, btn3)

    return markup


def help_keyboard_handler(message, bot=None):
    """
        Handle pressed button on first step of conversation.
        :param bot: object of telebot.TeleBot(BOT_TOKEN)
        :param message: input message
    """
    if message.text == 'Ввести название города':
        msg = bot.send_message(message.chat.id, 'Теперь введите название города с клавиатуры')
        lst_city_photos = get_city(msg.text)
        bot.send_message(message.chat.id, lst_city_photos)
        # bot.register_next_step_handler(msg, help_keyboard_handler_stp1())
    elif message.text == 'Определить по Вашим геоданным':
        # func2()
        pass
    elif message.text == 'Показать случайный':
        # func3()
        pass


def get_city(city_name):
    city = Cities.objects.get(city_name=city_name)
    return 'City name: {0}, City URL: {1}, Author of photos: {2}'.format(city.city_name,
                                                                         city.city_url,
                                                                         city.author)

