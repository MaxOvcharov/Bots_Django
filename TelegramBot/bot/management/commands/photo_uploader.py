# -*- coding: utf-8 -*

from __future__ import absolute_import
import httplib2
import sys
import os

from bot.models import Cities, CityPhotos

from django.core.management.base import BaseCommand
from TelegramBot.settings import BASE_DIR

import logging
logger = logging.getLogger('cron')

reload(sys)
sys.setdefaultencoding('utf-8')


class Command(BaseCommand):
    help = 'Upload photo from https://www.phototowns.ru web-site'

    def handle(self, *args, **options):
        """
            Upload photo from https://www.phototowns.ru web-site.
            Return: file storage
        """
        h = httplib2.Http('.cache')
        cities = Cities.objects.values_list('id', 'city_name_en')
        city = ''
        try:
            for city in cities:
                city_photos = list(CityPhotos.objects.filter(city=city[0]).values_list("photo_url", flat=True))
                for city_photo in city_photos:
                    current_dir = os.path.join(BASE_DIR, 'img', city[0], city_photo.split('/')[-1])
                    response, content = h.request(city_photo)
                    with open(current_dir, 'wb') as f:
                        f.write(content)
        except Exception, e:
            logger.error(str(e) + '--> {0}'.format(city[0]))
