from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.cache import cache
from django.template import RequestContext
from datetime import datetime
from stats.views import log
from .models import Floor, Room
# Create your views here. A view is a Python function that takes a web request and returns a web response.
from django.contrib.auth.decorators import login_required



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