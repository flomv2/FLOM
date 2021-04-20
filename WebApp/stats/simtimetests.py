from django import test
from django.test import Client
from django.test import TestCase
#import datetime
from .models import *
from .views import *
from datetime import date, datetime as dt
import pytz
from freezegun import freeze_time


"""
@call  'python3 manage.py test stats.simtimetests'

"""
class simulateTime(TestCase):
    #this only works if run on an empty database
    #for some reason uses the production database
    #clear it to run with python3 manage.py flush

    #if you need to access the webapp when running the server after flushing
    #create a user with 'python3 manage.py createsuperuser'
    #'admin admin' user will not exist after flushing

    '''
    killing it 
    assert(this works)
    '''

    c = Client()
    c.login(username='admin', password='admin')

    #day
    with freeze_time("2021-04-06 12:00:01"):
        c.get("http://127.0.0.1:8000/floor/enter/3/323C/pass")
    with freeze_time("2021-04-06 12:30:01"):
        c.get("http://127.0.0.1:8000/floor/exit/3/323C/pass")
    with freeze_time("2021-04-07 12:00:01"):
        time.sleep(10)
    temp = (get_stats('323C'))['day']
    assert(temp.count() == 1) #only 1 day object
    print("Day object successfully created")

    #month
    with freeze_time("2021-04-07 12:30:01"):
        c.get("http://127.0.0.1:8000/floor/enter/3/323C/pass")
    with freeze_time("2021-04-07 12:45:01"):
        c.get("http://127.0.0.1:8000/floor/exit/3/323C/pass")
    with freeze_time("2021-05-01 12:00:01"):
        time.sleep(10)
    temp = (get_stats('323C'))['month']
    assert(temp.count() == 1) #only 1 month object
    temp = (get_stats('323C'))['day']
    assert(temp.count() == 2) #only 2 days actually exist so far
    print("Month object successfully created")
    print("Multiple days created successfully")

    #year
    with freeze_time("2021-05-06 12:00:01"):
        c.get("http://127.0.0.1:8000/floor/enter/3/323C/pass")
    with freeze_time("2021-05-06 12:30:01"):
        c.get("http://127.0.0.1:8000/floor/exit/3/323C/pass")
    with freeze_time("2021-05-07 12:30:01"):
        time.sleep(10)
        c.get("http://127.0.0.1:8000/floor/enter/3/323C/pass")
    with freeze_time("2021-05-07 12:45:01"):
        c.get("http://127.0.0.1:8000/floor/exit/3/323C/pass")
    with freeze_time("2022-01-01 12:00:01"):
        time.sleep(10)
    temp = (get_stats('323C'))['year']
    assert(temp.count() == 1) #1 year created for 323C in 2021
    print("Year object successfully created")
    temp = (get_stats('323C'))['month']
    assert(temp.count() == 2) #2 months visited so far with freezegun
    print("Multiple months created successfully")
    temp = (get_stats('323C'))['day']
    assert(temp.count() == 4) #4 actual days visited with freezegun

    temp = "threadf works"
    assert(temp == "threadf works")
    print("Woohoo, it works")