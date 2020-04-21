import ast
import json

from django.test import TestCase
from . import views
from django.test import Client
from django.http import HttpResponse

"""
Need to figure out why authenticate() is failing and returning None when
we try to break up the test cases into methods in the class
"""

# Create your tests here.
class BasicTestCase(TestCase):
    #def test_valid_enter_exit(self):
    print("Testing simply entering and exiting a room that exists (311)")
    #Enter Room Success
    #Must Login to enter the room
    c = Client()
    response = c.post("http://127.0.0.1:8000/enter/3/311", {"username":"admin","password":"admin"})
    """
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    WARNING: PASSWORD CANNOT BE DISPLAYED IN CODE WHILE APP IS IN DEVELOPMENT
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    assert(response.status_code == 200)
    response_string = (response.content).decode('ASCII') #To String
    assert(response_string == "Room successfully entered!")
    
    #Exit Room
    response = c.post("http://127.0.0.1:8000/exit/3/311", {"username":"admin","password":"admin"} ) #Response is of type byte
    assert(response.status_code == 200)
    response_string = (response.content).decode('ASCII') #To String
    assert(response_string == "Room successfully exited!")
    print("Room successfully exited!")


# Create your tests here.
class WrongRoom(TestCase):
    #def test_nonexistant_room(self):
    print("Testing entering and exiting a room that does not exist (300)")
    #Enter Room Success
    #Must Login to enter the room
    c = Client()
    #Enter Room
    response = c.post("http://127.0.0.1:8000/enter/3/300", {"username":"admin","password":"admin"})#Response is of type byte
    response_string = (response.content).decode('ASCII') #To String
    assert(response.status_code == 404)
    assert(response_string == "Room Not Found")
    
    print("Room Not Found")
    #Exit Room
    response = c.post("http://127.0.0.1:8000/exit/3/300", {"username":"admin","password":"admin"} ) #Response is of type byte
    response_string = (response.content).decode('ASCII') #To String
    assert(response.status_code == 404)
    assert(response_string == "Room Not Found")
    
    print("Room Not Found")

# Create your tests here.

class DoneAlready(TestCase):
    print("Trying to enter and exit multiple times back to back")
    #Enter Room Success
    #Must Login to enter the room
    c = Client()
    #Enter Room
    response = c.post("http://127.0.0.1:8000/enter/3/311", {"username":"admin","password":"admin"})
    response = c.post("http://127.0.0.1:8000/enter/3/311", {"username":"admin","password":"admin"})
    response_string = (response.content).decode('ASCII') #To String
    assert(response.status_code == 409)
    assert(response_string == "Room already occupied")
    print("Room already occupied")
    #Exit Room
    response = c.post("http://127.0.0.1:8000/exit/3/311", {"username":"admin","password":"admin"} )
    response = c.post("http://127.0.0.1:8000/exit/3/311", {"username":"admin","password":"admin"} )
    response_string = (response.content).decode('ASCII') #To String
    assert(response.status_code == 409)
    assert(response_string == "Room already empty")
    print("Room already empty")


class AllRooms(TestCase):
    print("Going to enter and exit every room")
    #Load all of the rooms
    CONFIG_FILE = 'api/config.ini'
    config = {}
    with open(CONFIG_FILE) as cfile:
        config = json.load(cfile)
    #Login to exit and enter
    c = Client()
    #c.login(username='admin', password='admin')
    #Loop through all of the floors
    for floor in config["FLOORS"]:
        rooms = config["FLOORS"][floor]
        rooms = ast.literal_eval(rooms)
        print("On floor:", floor)
        #Loop through all of the rooms
        for room in rooms:
            #Enter the room
            response = c.post("http://127.0.0.1:8000/enter/{}/{}".format(floor,room), {"username":"admin","password":"admin"})
            assert(response.status_code == 200)
            #Exit the room
            response = c.post("http://127.0.0.1:8000/exit/{}/{}".format(floor,room), {"username":"admin","password":"admin"})
            assert(response.status_code == 200)
        print("All Rooms successfully exited and entered!!!")

