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
        'Mischbereifung': 'Mischbereifung',
        'CarPlay': 'CarPlay',
    }

    for k,v in cars['data'].items():
        if 'deleted' in v:
            print("deleted at %s" % v['deleted']);
        found_equipment = {}
        for dk,dv in desired_eq.items():
            found_equipment[dk] = False
            for e in v['data']['equipment']:
                if dv in e:
                    found_equipment[dk] = True
                    break
        cars['data'][k]['found_equipment'] = found_equipment
    
    def byOrderId(e):
        return e['id']


    deleted = list(filter(lambda c: 'deleted' in c, cars['data'].values()))
    deleted.sort(key=byOrderId, reverse=True)

    actual = list(filter(lambda c: 'deleted' not in c, cars['data'].values()))
    actual.sort(key=byOrderId, reverse=True)

    template = loader.get_template('carview/index.html')
    context = {
        'actual': actual,
        'deleted': deleted,
        'desired_eq': desired_eq,
        'info': { 'query': cars['query'],
                  'updated': cars['updated'],
        }
    }
    return HttpResponse(template.render(context, request))

