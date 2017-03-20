# -*- coding: utf-8 -*

from __future__ import absolute_import
import sys
import datetime
import telebot

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from bot.keyboards import inline_news_vote
from bot.models import UserInfo, News, NewsPoll
from TelegramBot.settings import BOT_TOKEN

import logging
logger = logging.getLogger('cron')

reload(sys)
sys.setdefaultencoding('utf-8')
bot = telebot.TeleBot(BOT_TOKEN)


class Command(BaseCommand):
    help = 'Send news by the list of users'

    def handle(self, *args, **options):
        """
            Send news by the list of users on the post date.
            Checks if news doesn't published, then send to
            users (15/sec).
            Return: None
        """
        logger.info('Start send news')
        today = datetime.datetime.today()
        user_chat_ids = UserInfo.objects.values_list('chat_id', flat=True)
        try:
            news_to_post = list(News.objects.filter(published=True).
                                filter(Q(post_date__lte=today) | Q(post_date=None)))
            for news in news_to_post:
                for chat_id in user_chat_ids:
                    bot.send_message(chat_id=chat_id,
                                     text=news.content,
                                     reply_markup=inline_news_vote())
            logger.info('End send news')
        except ObjectDoesNotExist, e:
            logger.error('Handle ERROR: {0}'.format(e))
        except Exception, e:
            logger.error('Handle ERROR: {0}'.format(e))
