from datetime import datetime
from django.http import HttpResponse
from django.template import loader
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from tools.persistent import load

def cars(request):
    cars = load()

    desired_eq = {
        'Panoramadach': 'Panorama Glasdach',
        'Active cruise': 'Aktive',
        'HUD': 'Display',
        'Rückfahrkamera': 'Rückfahrkamera',
        'Surround View': 'Surround',
        'Spurwechselwarnung': 'Spurwechselwarnung',
        'Sitzheizung': 'Sitzheizung',
        'Sitzverstellung': 'Sitzverstellung',
        'M Sportpaket':  'M Sportpaket',
        'Sitzheizung': 'Sitzheizung',
        'Wireless charging': 'Wireless Charging',
        'Harman Kardon HiFi': 'Harman Kardon',
        'Komfortzugang': 'Komfortzugang',
        'Alu Leisten': 'Alu',
        'Mischbereifung': 'Mischbereifung'
    }

    for k,v in cars.items():
        found_equipment = {}
        for dk,dv in desired_eq.items():
            found_equipment[dk] = False
            for e in v['data']['equipment']:
                print("in %s" % e)
                if dv in e:
                    found_equipment[dk] = True
                    break
        cars[k]['found_equipment'] = found_equipment
    
    template = loader.get_template('carview/index.html')
    context = {
        'cars340': filter(lambda c: '340' in c['data']['name'], cars.values()),
        'cars330': filter(lambda c: '330' in c['data']['name'], cars.values()),
        'desired_eq': desired_eq,
    }
    return HttpResponse(template.render(context, request))

