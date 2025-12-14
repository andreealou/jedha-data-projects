import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import plotly.express as px
import numpy as np
import json
import re
from urllib.parse import quote_plus
from urllib.parse import unquote_plus  # tweak: décoder + gère les '+'

# Liste des villes
df = pd.read_csv("classement_villes_pour_hotels.csv")
list_top_cities = df['Ville'].astype(str).tolist()


class Spider_booking(scrapy.Spider):
    name = 'booking_spider'
    allowed_domains = ['booking.com']
    
    handle_httpstatus_list = [200, 202]  # on veut traiter aussi les 202
    custom_settings = {
    "COOKIES_ENABLED": True,   # garder les cookies de consentement
    }
    
    start_urls = [
        f"https://www.booking.com/searchresults.fr.html?ss={quote_plus(city)}&rows=25&order=popularity"
        for city in list_top_cities
    ]
    
    def parse(self, response):       
        hotels_names = response.xpath("//h3/a/div[1]/text()").getall()
        relative_urls = response.xpath("//h3/a/@href").getall()
    
        # Fallback XPath
        if not hotels_names or not relative_urls:
            hotels_names = response.xpath("//div[@data-testid='property-card']//*[ @data-testid='title']/text()").getall()
            relative_urls = response.xpath("//div[@data-testid='property-card']//*[ @data-testid='title']/@href").getall()

        hotels_names = hotels_names[:20]
        relative_urls = relative_urls[:20]

        for hotel_name, hotel_url in zip(hotels_names, relative_urls):
            city_name = response.url.split('ss=')[1].split('&')[0]
            city_name = unquote_plus(city_name)

            yield response.follow(
                hotel_url,
                callback=self.parse_hotel,
                meta={
                    'hotel_name': hotel_name.strip() if hotel_name else None,
                    'city_name': city_name
                }
            )


    def parse_hotel(self, response):
        city_name = response.meta['city_name']

        # SCORE : essayer plusieurs sélecteurs en cascade
        hotel_score_text = (
        response.xpath('//div[@data-testid="review-score-right-component"]/div[@aria-hidden="true"]/text()').get()
        or response.css('[data-testid="review-score"]::text').get()
        or response.css('[data-testid="external-review-score"]::text').get()
        or response.css('[data-testid="review-score-subcomponent"]::text').get()
        )
        # Nettoyage si trouvé, sinon "N/A"
        hotel_score_text = hotel_score_text.strip() if hotel_score_text else 'N/A'

        # DESCRIPTION : essayer plusieurs sélecteurs en cascade
        description_text = (
            " ".join(d.strip() for d in response.css('[data-testid="property-description"]::text').getall() if d.strip())
            or " ".join(d.strip() for d in response.css('#property_description_content p::text').getall() if d.strip())
            or response.xpath("//meta[@name='description']/@content").get()
        )
        # Nettoyage si trouvé, sinon "N/A"
        description_text = description_text.strip() if description_text else 'N/A'

        # LATITUDE et LONGITUDE : fallbacks en cascade
        latlng = (
            response.css('[data-atlas-latlng]::attr(data-atlas-latlng)').get()
            or response.css('meta[property="booking_com:location:latitude"]::attr(content)').get() + "," +
            response.css('meta[property="booking_com:location:longitude"]::attr(content)').get()
            or response.css('[data-lat]::attr(data-lat)').get() + "," +
            response.css('[data-lon]::attr(data-lon)').get()
        )

        latitude, longitude = (None, None)
        if latlng and "," in latlng:
            parts = latlng.split(",", 1)
            latitude = parts[0].strip() if parts[0] else None
            longitude = parts[1].strip() if len(parts) > 1 else None

     
        yield {
            'City': city_name,
            'Hotel_name': response.meta['hotel_name'],
            'Hotel_url': response.url,
            'Hotel_score': hotel_score_text,
            'Hotel_description': description_text,
            'Latitude': latitude,
            'Longitude': longitude,
        }

filename = "Destinations_infos.json" # Fichier sauvegarde

if filename in os.listdir():
    os.remove(filename) # Si jamais le nom existe deja

process = CrawlerProcess(settings={
    'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.1 Safari/537.36",
    'LOG_LEVEL': logging.DEBUG,
    'AUTOTHROTTLE_ENABLED': True,
    'DOWNLOAD_DELAY': 1.0,
    'COOKIES_ENABLED': False,   # <- tu peux laisser False ici, on force True seulement dans la classe (Étape 1)
    'DEFAULT_REQUEST_HEADERS': {
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.booking.com/',
    },
    'FEEDS': {"Destinations_infos.json": {"format": "json"}}
})

process.crawl(Spider_booking)
process.start()