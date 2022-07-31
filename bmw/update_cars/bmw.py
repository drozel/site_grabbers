import os, sys

from .get_cars import *
from datetime import *

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from tools.persistent import *
from tools.download import *

def hookNewCar(car_data):
    print("new car available: %s" % car_data['data']['name'])

def hookCarDeleted(car_data):
    print("car sold: %s" % car_data['data']['name'])

def update(force=False):
    # get cars for the query
    cars = getCarsList("https://gebrauchtwagen.bmw.de/nsc/search?q=:creationDateSort-desc:attributes-bodyType:Gran%20Turismo:series:3:model:330:model:340:environment-fuelType:Benzin:drivingAssistance-rearViewCamera:true:interiorDesign-electronicSeatAdjustment:true:entertainmentCommunication-navigationsystemProfessional:true:equipment-mSportPackage:true")
    print("currently %d cars available" % len(cars))

    # load known cars
    known_cars = load()
    if not known_cars:
        known_cars = {}
    print(known_cars.keys())

    # find new cars
    for id, url in cars.items():
        if id not in known_cars.keys():
            car_data = {}
            car_data['added'] = datetime.now()
            car_data['data'] = getCarDetails(url)
            car_data['url'] = 'https://gebrauchtwagen.bmw.de/%s' % url
            car_data['id'] = id
            hookNewCar(car_data)
            download(car_data['data']['picture_link'], 'data/pictures/%s.png' % id)
            known_cars[id] = car_data
        if force:
            print('force update car %s' % id)
            known_cars[id]['data'] = getCarDetails(url)

    # check deleted ones
    for id,data in known_cars.items():
        if id not in cars.keys() and 'deleted' not in data: 
            data['deleted'] = datetime.now()
            hookCarDeleted()

    # save current state
    save(known_cars)
    print('%d cars known' % len(known_cars))

if __name__=="__main__":
    main()
