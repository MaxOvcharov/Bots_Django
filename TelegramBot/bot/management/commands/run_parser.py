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
        city_name = ''
        try:
            logger.info('Start parser')
            r = requests.get('https://www.phototowns.ru/all')
            soup = BeautifulSoup(r.text)
            cities = soup.findAll('div', style='width: 200px; height: 300px; float: left; margin: 10px;')
            city_href = [city.findAll('a') for city in cities]

            for href in city_href:
                city_name = href[1]['title'].encode('utf-8')
                city_name = re.split(' \\(|\\.| \xd0\xb8', city_name)[0]
                city_url = href[1]['href'].encode('utf-8')
                author = href[2].findAll('a', text=re.compile(r'.*'))[0].encode('utf-8')
                r = requests.get(city_url)
                soup = BeautifulSoup(r.text)
                images = soup.findAll('dl', {'class': 'gallery-item'})[0:10]
                images_href = [url.findAll('a')[0]['href'] for url in images]
                # get TOP 10 images urls
                img_url_lst = get_img_urls(images_href)
                # get city name in English
                city_name_en = get_city_name_en(city_name)
                # Update or create Cities table
                update_city = {'city_name': city_name,
                               'city_name_en': city_name_en['city'],
                               'geo_latitude_min': city_name_en['latitude_min'],
                               'geo_latitude_max': city_name_en['latitude_max'],
                               'geo_longitude_min': city_name_en['longitude_min'],
                               'geo_longitude_max': city_name_en['longitude_max'],
                               'city_url': city_url,
                               'author': author}
                update_cities_table(update_city)
                # Update or create City_photos table
                update_city_photos_table(img_url_lst, city_name, author)
            logger.info('All cities are updated')
        except Exception, e:
            logger.error(str(e) + '--> {0}'.format(city_name))


def get_city_name_en(city_name):
    """
        Get city name (Eng) by city name(Ru)
        :param city_name: city name(Ru)
        :return: Dict of city name(Eng), location(latitude), location(longitude)
    """
    geo_data = {}
    try:
        g = geocoder.yandex(city_name)
        geo_data['city'] = str(g.json['city']).encode('utf-8')
        geo_data['longitude_min'] = g.json['bbox']['southwest'][1]
        geo_data['longitude_max'] = g.json['bbox']['northeast'][1]
        geo_data['latitude_min'] = g.json['bbox']['southwest'][0]
        geo_data['latitude_max'] = g.json['bbox']['northeast'][0]
        return geo_data
    except Exception, e:
        logger.error(str(e) + '-->City name: {0} and  Geo data: {1}'.format(city_name, geo_data))


def get_img_urls(images_href):
    """
        Get image url from html <a href="..."> tag
        :param images_href: list of html <a href="..."> tag
        :return: list of image urls
    """
    try:
        img_lst = []
        for image in images_href:
            r = requests.get(image)
            soup = BeautifulSoup(r.text)
            images_urls = soup.findAll('div', {'class': 'big_pic'})[0].findAll('img')[0]['src']
            img_lst.append(images_urls)
        return img_lst
    except Exception, e:
        logger.error(str(e) + '--> {0}'.format(images_href))


def update_cities_table(update_city):
    """
        Update or create Cities table
        :param update_city: all Cities table fields
        :return: None
    """
    try:
        Cities.objects.update_or_create(city_name=update_city['city_name'],
                                        city_name_en=update_city['city_name_en'],
                                        geo_latitude_min=update_city['geo_latitude_min'],
                                        geo_latitude_max=update_city['geo_latitude_max'],
                                        geo_longitude_min=update_city['geo_longitude_min'],
                                        geo_longitude_max=update_city['geo_longitude_max'],
                                        city_url=update_city['city_url'],
                                        author=update_city['author'],
                                        defaults=update_city)
    except Exception:
        Cities.objects.filter(city_name_en=update_city['city_name_en']).update(city_name=update_city['city_name'])


def update_city_photos_table(img_url_lst, city_name, author):
    """
        Update or create CityPhotos table
        :param img_url_lst: list of image urls
        :param city_name: city name
        :param author: photos author name
        :return: None
    """
    try:
        city_id = Cities.objects.get(city_name=city_name, author=author)
        for url in img_url_lst:
            update_photos = {'photo_url': url, 'city_id': city_id}
            CityPhotos.objects.update_or_create(photo_url=url,
                                                city_id=city_id,
                                                defaults=update_photos)
    except Cities.DoesNotExist:
        # ignore duplicate city ID
        pass
    except CityPhotos.DoesNotExist, e2:
        logger.error(str(e2) + '--> {0}'.format(city_name))

