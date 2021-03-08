import ast
import json

from django.test import TestCase
from . import views
from django.test import Client
from django.http import HttpResponse

# Create your tests here.
class BasicTestCase(TestCase):
    print("Testing simply entering and exiting a room that exists (311)")
    #Enter Room Success
    #Must Login to enter the room
    c = Client()
    c.login(username='admin', password='admin')
    #Enter Room
    response = c.get("http://127.0.0.1:8000/floor/enter/3/311/pass") #Response is of type byte
    response_string = (response.content).decode('ASCII') #To String
    assert(response_string == "Room successfully entered!")
    print("Room successfully entered!")
    #Exit Room
    response = c.get("http://127.0.0.1:8000/floor/exit/3/311/pass") #Response is of type byte
    response_string = (response.content).decode('ASCII') #To String
    assert(response_string == "Room successfully exited!")
    print("Room successfully exited!")

# Create your tests here.
class WrongRoom(TestCase):
    print("Testing entering and exiting a room that does not exist (300)")
    #Enter Room Success
    #Must Login to enter the room
    c = Client()
    c.login(username='admin', password='admin')
    #Enter Room
    response = c.get("http://127.0.0.1:8000/floor/enter/3/300/pass") #Response is of type byte
    response_string = (response.content).decode('ASCII') #To String
    assert(response_string == "Room Not Found")
    print("Room Not Found")
    #Exit Room
    response = c.get("http://127.0.0.1:8000/floor/exit/3/300/pass") #Response is of type byte
    response_string = (response.content).decode('ASCII') #To String
    assert(response_string == "Room Not Found")
    print("Room Not Found")

# Create your tests here.
class DoneAlready(TestCase):
    print("Trying to enter and exit multiple times back to back")
    #Enter Room Success
    #Must Login to enter the room
    c = Client()
    c.login(username='admin', password='admin')
    #Enter Room
    response = c.get("http://127.0.0.1:8000/floor/enter/3/311/pass") #Response is of type byte
    response = c.get("http://127.0.0.1:8000/floor/enter/3/311/pass") #Response is of type byte
    response_string = (response.content).decode('ASCII') #To String
    assert(response_string == "Room already occupied")
    print("Room already occupied")
    #Exit Room
    response = c.get("http://127.0.0.1:8000/floor/exit/3/311/pass") #Response is of type byte
    response = c.get("http://127.0.0.1:8000/floor/exit/3/311/pass") #Response is of type byte
    response_string = (response.content).decode('ASCII') #To String
    assert(response_string == "Room already empty")
    print("Room already empty")


class AllRooms(TestCase):
    print("Going to enter and exit every room")
    #Load all of the rooms
    CONFIG_FILE = 'WebApp/config.ini'
    config = {}
    with open(CONFIG_FILE) as cfile:
        config = json.load(cfile)
    #Login to exit and enter
    c = Client()
    c.login(username='admin', password='admin')
    #Loop through all of the floors
    for floor in config["FLOORS"]:
        rooms = config["FLOORS"][floor]
        rooms = ast.literal_eval(rooms)
        print("On floor:", floor)
        #Loop through all of the rooms
        for room in rooms:
            #Enter the room
            response = c.get("http://127.0.0.1:8000/floor/enter/{}/{}/pass".format(floor,room))
            #Exit the room
            response = c.get("http://127.0.0.1:8000/floor/exit/{}/{}/pass".format(floor,room))
        print("All Rooms successfully exited and entered!!!")
