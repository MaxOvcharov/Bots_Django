# -*- coding: utf-8 -*

from __future__ import absolute_import
import sys

# from bot.models import Test - you can use all django methods
from django.core.management.base import BaseCommand

import logging
logger = logging.getLogger('cron')

reload(sys)
sys.setdefaultencoding('utf-8')


class Command(BaseCommand):
    help = 'Your description here'

    def handle(self, *args, **options):
        """
            Your description here
        """
        try:
            logger.info('Start test command')
            pass
            logger.info('End test command')
        except Exception, e:
            logger.error(e)


