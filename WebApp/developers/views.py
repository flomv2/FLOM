from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.cache import cache
from django.template import RequestContext
from datetime import datetime
from stats.views import log
from .models import Floor, Room
# Create your views here. A view is a Python function that takes a web request and returns a web response.
from django.contrib.auth.decorators import login_required



#TODO: learn what actually gets put in on a page request

floors = {} # floor['3'] = Floor('floor3') and same for 4
rooms = {} # holds the rooms for all the floors

def getUpdatedRoomsList(floor):
	'''
	Creates an updated version of the rooms list used for updating the webpage
	@return a dictionary with (key = "Rooms", value = list of rooms and their occupancy)
	'''
	# create an empty dictionary and add key "Rooms" with empty list as value
	roomList = {}
	roomList["Rooms"] = []
	# iterate through all the rooms on the floor
	# 	get room data to add
	# 	append room data to roomList
	for room in floor.room_set.all():
		add = {"ID": room.roomID, "occupied" : room.occupied}
		roomList["Rooms"].append(add)
	return roomList

@login_required
def index(request, floor):
	'''
	@return the display for floor
	'''
	return cache.get("display" + floor)

@login_required
def enterRoom(request, floor, ID, password):
	'''
	This function is called when someone enters a room
	@modifies Room object with matching ID
	@return Response to server
	'''
	# Check for room existence
	if ID in rooms.keys():
		currRoom = rooms[ID]
		# if the current room is already occupied
		if currRoom.occupied:
			return HttpResponse("Room already occupied")
		else:
			# modify current room to occupied = True and update current datetime
			currRoom.occupied = True
			currRoom.lastEntered = datetime.now()
			log(ID,1)
			# save changes made to current room (to database)
			currRoom.save()
			# create the dictionary of rooms needed to update webpage
			roomList = getUpdatedRoomsList(floors[floor])
			# set the cache with the new room display based on changes made
			display = render_to_response('floor/templates/html/floor' + floor + '.html', roomList)
			cache.set("display" + floor, display, None)
			return HttpResponse("Room successfully entered!")
	# Room not found
	else:
		return HttpResponse("Room Not Found")

@login_required
def exitRoom(request, floor, ID, password):
	'''
	This function is called when someone exits a room
	@modifies Room object with matching ID
	@return Response to server
	'''
	# Check for room existence
	if ID in rooms.keys():
		currRoom = rooms[ID]
		# if the room is empty
		if not currRoom.occupied:
			return HttpResponse("Room already empty")
		else:
			# modify current room to occupied = False and update current datetime
			currRoom.occupied = False
			currRoom.lastExited = datetime.now()
			log(ID,0)
			# save changes made to current room (to database)
			currRoom.save()
			# create dictionary of rooms needed to update webpage
			roomList = getUpdatedRoomsList(floors[floor])
			# set the cache with the new room display based on changes made
			display = render_to_response('floor/templates/html/floor' + floor + '.html', roomList)
			cache.set("display" + floor, display, None)
			return HttpResponse("Room successfully exited!")
	# Room not found
	else:
		return HttpResponse("Room Not Found")

def createRooms(floor, IDs):
	'''
	Creates the rooms for an individual floor. If the Room with the ID exists, its pulled from
	the database. Otherwise a new Room is created and assigned to the floor.
	The roomsList gets generated for the floor and the display is set in the cache.
	'''
	for ID in IDs:
		roomFound = Room.objects.filter(roomID=ID).count()
		if roomFound > 0:
			rooms[ID] = Room.objects.get(roomID=ID)
		else:
			# create new Room with corresponding floor
			rooms[ID] = Room(roomID=ID, occupied=False, lastEntered=datetime.now(), lastExited=datetime.now(), floor=floor)
			rooms[ID].save()
			floor.roomCount += 1
			floor.save()
	roomList = getUpdatedRoomsList(floor)
	display = render_to_response('floor/templates/html/' + floor.name + '.html', roomList)
	cache.set('display'+floor.name[-1], display, None)

def populateFloors():
	'''
	Fills the rooms dictionary with key = {ID}, value = {Room} (see Room object definition in models.py)
	Should only be called once at startup
	@modifies rooms
	'''
	# get the room IDs from the cache for the floor
	floor3IDs = cache.get('floor3')
	floor4IDs = cache.get('floor4')
	floor3Found = Floor.objects.filter(name='floor3').count()
	if floor3Found > 0:
		floor3 = Floor.objects.get(name='floor3')
	else:
		floor3 = Floor(name='floor3')
		floor3.save()
	floor4Found = Floor.objects.filter(name='floor4').count()
	if floor4Found > 0:
		floor4 = Floor.objects.get(name='floor4')
	else:
		floor4 = Floor(name='floor4')
		floor4.save()
	floors['3'] = floor3
	floors['4'] = floor4
	print('Creating rooms for floor 3...')
	createRooms(floor3, floor3IDs)
	print('Creating rooms for floor 4...')
	createRooms(floor4, floor4IDs)