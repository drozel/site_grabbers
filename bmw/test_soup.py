import urllib.request as urllib2
from bs4 import *
from urllib.parse  import urljoin
import sys

try:
    full_url = 'https://gebrauchtwagen.bmw.de//nsc/Fahrzeuge/BMW/3er/340/340i-Gran-Turismo/p/10208132?q=:creationDateSort-desc:attributes-bodyType:Gran+Turismo:series:3:model:330:model:340:environment-fuelType:Benzin:drivingAssistance-rearViewCamera:true:interiorDesign-electronicSeatAdjustment:true:equipment-mSportPackage:true'
    c = urllib2.urlopen(full_url)
except:
    eprint( "Could not open car's site")


car_soup = BeautifulSoup(c.read(), "html.parser")

car = {}
# car['name'] = car_soup.find('div', class_='col-flex pdp-details-top-title').find('h1')
# car['order_nr'] = car_soup.find('div', class_='col-flex pdp-details-top-title').find('p')
# car['price'] = car_soup.find('div', class_='pdp-details-top-info-price').find('span', class_="bigger")
# car['registration'] = car_soup.select("[data-feature-icon='firstregistration']")[0].find('span')
# car['mileage'] = car_soup.select("[data-feature-icon='mileage']")[0].find('span')
print(car_soup.find('a', class_='js-plan-dealer-route dealer-info-inner--block-address',href=True))
print(car_soup.find_all('a', class_='js-plan-dealer-route dealer-info-inner--block-address'))
car['picture_link'] = car_soup.find('picture').find('img')['src']
car['picture_fake'] = len(car_soup.find_all('div', string='Abbildung')) > 0

print(car)