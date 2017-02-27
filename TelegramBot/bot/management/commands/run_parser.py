# -*- coding: utf-8 -*

from __future__ import absolute_import
import geocoder
import re
import requests
import sys

from BeautifulSoup import BeautifulSoup
from bot.models import Cities, CityPhotos
from django.core.management.base import BaseCommand

import logging
logger = logging.getLogger('cron')

reload(sys)
sys.setdefaultencoding('utf-8')


class Command(BaseCommand):
    help = 'Get content from https://www.phototowns.ru web-site'

    def handle(self, *args, **options):
        """
            Get content from https://www.phototowns.ru web-site:
                - list of Russian cities
                - Top 10 photo of each city
                - Author of photos
            Return: dict of contents
        """
        try:
            logger.info('Start parser')
            r = requests.get('https://www.phototowns.ru/all')
            soup = BeautifulSoup(r.text)
            cities = soup.findAll('div', style='width: 200px; height: 300px; float: left; margin: 10px;')
            city_href = [city.findAll('a') for city in cities]

            for href in city_href:
                city_name = href[1]['title'].encode('utf-8')
                city_url = href[1]['href'].encode('utf-8')
                author = href[2].findAll('a', text=re.compile(r'.*'))[0].encode('utf-8')
                r = requests.get(city_url)
                soup = BeautifulSoup(r.text)
                images = soup.findAll('dl', {'class': 'gallery-item'})[0:10]
                images_href = [url.findAll('a')[0]['href'] for url in images]
                img = []
                for image in images_href:
                    r = requests.get(image)
                    soup = BeautifulSoup(r.text)
                    images_urls = soup.findAll('div', {'class': 'big_pic'})[0].findAll('img')[0]['src']
                    img.append(images_urls)
                city_name_en = get_city_name_en(city_name)
                # Insert content into DB
                update_city = {'city_name': city_name,
                               'city_name_en': city_name_en['city'],
                               'geo_latitude': city_name_en['latitude'],
                               'geo_longitude': city_name_en['longitude'],
                               'city_url': city_url,
                               'author': author}
                Cities.objects.update_or_create(city_name=city_name,
                                                city_name_en=city_name_en['city'],
                                                geo_latitude=city_name_en['latitude'],
                                                geo_longitude=city_name_en['longitude'],
                                                city_url=city_url,
                                                author=author,
                                                defaults=update_city)

                city_id = Cities.objects.get(city_name=city_name, author=author)
                for url in img:
                    update_photos = {'photo_url': url, 'city_id': city_id}
                    CityPhotos.objects.update_or_create(photo_url=url,
                                                        city_id=city_id,
                                                        defaults=update_photos)
            logger.info('All cities are updated')
        except Exception, e:
            logger.error(e)


def get_city_name_en(city_name):
    result = {}
    g = geocoder.google(city_name)
    result['city'] = str(g.geojson['properties']['city']).encode('utf-8')
    result['latitude'] = g.geojson['geometry']['coordinates'][0]
    result['longitude'] = g.geojson['geometry']['coordinates'][1]
    return result



