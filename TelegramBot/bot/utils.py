# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
import telebot
from telebot import types

from models import Cities, CityPhotos
from TelegramBot.settings import BOT_TOKEN


logger = logging.getLogger('telegram')

bot = telebot.TeleBot(BOT_TOKEN)

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


def help_keyboard_handler(message):
    """
        Handle pressed button on first step of conversation.
        :param message: input message
    """
    if message.text == u'Ввести название города':
        logger.debug(message.text)
        msg = bot.send_message(message.chat.id, 'Теперь введите название города с клавиатуры')
        logger.debug(msg)
        try:
            bot.register_next_step_handler(msg, get_city)
        except Exception as e:
            logger.error(e)
	    bot.reply_to(message, 'oooops')
	#bot.send_message(message.chat.id, lst_city_photos)
        # bot.register_next_step_handler(msg, help_keyboard_handler_stp1())
    elif str(message.text).encode('utf-8') == 'Определить по Вашим геоданным':
        # func2()
        pass
    elif str(message.text).encode('utf-8') == 'Показать случайный':
        # func3()
        pass


def get_city(message):
    logger.debug(message.text)
    #city_name = str(message.text).encode('utf-8')
    #logger.debug(type(city_name))
    '''
    try:
        city = Cities.objects.get(city_name=city_name)
	bot.send_message(message.chat.id, 'City name: {0}, City URL: {1}, Author of photos: {2}'.format(city.city_name, city.city_url, city.author))
    except DoesNotExist, e:
	bot.send_message(message.chat.id, 'К сожалению нет такого города... :(')
    '''
