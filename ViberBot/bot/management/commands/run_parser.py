# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from django.core.management.base import BaseCommand, CommandError

from BeautifulSoup import BeautifulSoup

from bot.models import Cities, CityPhotos


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
            images = soup.findAll('dl', {'class': 'gallery-item'})
            images_urls = [url.findAll('a')[0].findAll('img')[0]['src'].encode('utf-8') for url in images]
            if len(images_urls) > 10:
                img = images_urls[0:10]
            else:
                img = images_urls
            update_city = {'city_name': city_name,
                           'city_url': city_url,
                           'author': author}

            obj, created = Cities.objects.update_or_create(city_name=city_name,
                                            city_url=city_url,
                                            author=author,
                                            defaults=update_city)
	    #print obj, created
            city_id = Cities.objects.get(city_name=city_name)
            for url in img:
                update_photos = {'photo_url': url, 'city_id': city_id.id}
                obj1, created1 = CityPhotos.objects.update_or_create(photo_url=url,
                                                    city_id=city_id.id,
                                                    defaults=update_photos)
		#print obj1, created1




