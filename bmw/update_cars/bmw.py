import os, sys

from .get_cars import *
from datetime import *

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from tools.persistent import *
from tools.download import *

main_query = "https://gebrauchtwagen.bmw.de/nsc/search?q=:creationDateSort-desc:attributes-bodyType:Gran%20Turismo:series:3:model:330:model:340:environment-fuelType:Benzin:drivingAssistance-rearViewCamera:true:entertainmentCommunication-navigationsystemProfessional:true"

def hookNewCar(car_data):
    print("new car available: %s" % car_data['data']['name'])

def hookCarDeleted(car_data):
    print("car sold: %s" % car_data['data']['name'])

def update(force=False):
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/pictures'):
        os.mkdir('data/pictures')
        
    # get cars for the query
    cars = getCarsList(main_query)
    print("currently %d cars available on the site" % len(cars))

    # load known cars
    known_cars = load()
    if not known_cars:
        known_cars = {}

    # check if should update DB completely
    if 'data_version' not in known_cars:
        known_cars['data_version'] = "unknown"
    if 'query' not in known_cars:
        known_cars['query'] = ""
    if 'data' not in known_cars:
        known_cars['data'] = {}

    if known_cars['data_version'] != data_version():
        print('data version changed (%s to %s)' % (known_cars['data_version'], data_version()))
        force = True

    if known_cars['query'] != main_query:   
        print('query changed (%s to %s)' % (known_cars['query'], main_query))
        force = True

    # find new cars
    for id, url in cars.items():
        if id not in known_cars['data'].keys() or force:
            car_data = {}
            if 'added' not in car_data:
                car_data['added'] = datetime.now()
            car_data['data'] = getCarDetails(url)
            car_data['url'] = 'https://gebrauchtwagen.bmw.de/%s' % url
            car_data['id'] = id
            hookNewCar(car_data)
            download(car_data['data']['picture_link'], 'data/pictures/%s.png' % id)
            known_cars['data'][id] = car_data

    # check deleted ones
    for id,data in known_cars['data'].items():
        if id not in cars.keys() and 'deleted' not in data: 
            data['deleted'] = datetime.now()
            hookCarDeleted(data)
            known_cars['data'][id] = data


    # save current state
    known_cars['data_version'] = data_version()
    known_cars['query'] = main_query
    known_cars['updated'] = datetime.now()
    save(known_cars)
    print('%d cars in the db' % len(known_cars['data']))