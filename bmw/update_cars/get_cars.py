#!/bin/python3

import urllib.request as urllib2
from bs4 import *
from urllib.parse  import urljoin

import re
import sys

import bs4
from django.test import tag

CLEANR = re.compile('<.*?>') 

def clean(raw, key=False):
  cleantext = str(raw)
  cleantext = re.sub(CLEANR, '', cleantext)
  cleantext = cleantext.replace('\n', '')
  cleantext = cleantext.replace('\r', '')
  cleantext = cleantext.replace('\t', '')
  cleantext = cleantext.replace('\xa0', '')
  cleantext = cleantext.strip()
  if key:
      cleantext = cleantext.replace('-', '')
      cleantext = cleantext.replace(' ', '')
  return cleantext
  
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def getCarsList(url):
    try:
        c = urllib2.urlopen(url)
    except:
        eprint( "Could not open the overview site %s" % url)

    links = {}
    for car_data in BeautifulSoup(c.read(), "html.parser").find_all(class_="product-list-item"):
        link = car_data.find('a', class_="name")['href']
        id = car_data.find('a', class_="addToCarpark")['data-productcode']
        links[id] = link

    print('{0} cars found'.format(len(links)))

    return links

def getCarDetails(url):
    try:
        full_url = 'https://gebrauchtwagen.bmw.de/%s' % url
        c = urllib2.urlopen(full_url)
    except:
        eprint( "Could not open car's site" % url)

    car_soup = BeautifulSoup(c.read(), "html.parser")

    car = {}
    car['name'] = car_soup.find('div', class_='col-flex pdp-details-top-title').find('h1')
    car['order_nr'] = car_soup.find('div', class_='col-flex pdp-details-top-title').find('p')
    car['price'] = car_soup.find('div', class_='pdp-details-top-info-price').find('span', class_="bigger")
    car['registration'] = car_soup.select("[data-feature-icon='firstregistration']")[0].find('span')
    car['mileage'] = car_soup.select("[data-feature-icon='mileage']")[0].find('span')
    car['location'] = ''.join(filter(lambda el: isinstance(el, str), car_soup.find('a', class_='js-plan-dealer-route dealer-info-inner--block-address').contents))
    car['picture_link'] = car_soup.find('picture').find('img')['src']
    car['picture_fake'] = len(car_soup.find_all('div', string='Abbildung ähnlich')) > 0

    car['feature'] = {}
    for feature in car_soup.find_all('div', class_="vehicle-details-panel-feature"):
        name = feature.find('div', class_='vehicle-details-panel-feature-name')
        value = feature.find('div', class_='vehicle-details-panel-feature-value')
        if not value:
            continue # premium selection icon ><

        car['feature'][clean(name, True)] = clean(value.find('span'))

    car['equipment'] = []
    for eq_panel in car_soup.select("[class='equipment-panel-content']"):
        for eq in eq_panel.find_all('span'):
            car['equipment'].append(clean(eq))

    # convert all to string, clean html
    for k,v in car.items():
        if not isinstance(v, bs4.Tag):
            continue
        if 'link' in k:
            continue

        car[k] = clean(str(v))
        
    return car