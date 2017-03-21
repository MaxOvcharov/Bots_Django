import sys
import telebot

from django.core.management.base import BaseCommand
from TelegramBot.settings import BOT_TOKEN, WEBHOOK_HOST


import logging
logger = logging.getLogger('cron')

reload(sys)
sys.setdefaultencoding('utf-8')


class Command(BaseCommand):
    help = 'Set web-hook for your domain/IP'

    def handle(self, *args, **options):
        """
            Set web-hook for your domain/IP
        """
        try:
            logger.debug('Set web-hook')
            bot = telebot.TeleBot(BOT_TOKEN)
            bot.remove_webhook()
            bot.set_webhook(url='https://{bot_url}/bot/{bot_token}/'
                            .format(bot_token=BOT_TOKEN, bot_url=WEBHOOK_HOST))
            logger.debug('Web-hook is set')
        except Exception, e:
            logger.error(e)
