from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.cache import cache
from django.template import RequestContext
from datetime import datetime
#from stats.views import log
from .models import Floor, Room
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from stats.views import log
# Create your views here. A view is a Python function that takes a web request and returns a web response.
#from django.contrib.auth.decorators import login_required



"""
TODO: Change this to a post request
have user and password in post request body instead
of url

"""
@api_view(['POST'])
def enterRoom(request, floor, ID):
	'''
	This function is called when someone enters a room
	@modifies Room object with matching ID
	@return Response to server
	'''
	data = request.data

	username = ''
	password = ''

	try:
		username = data['username']
		password = data['password']
	except:
		return HttpResponse("Please supply username and password in body",status= 401)

	#use post data information

	user = authenticate(username=username, password=password)

	if user is not None:
		pass
		# Continue execution
	else:
		return HttpResponse("Unauthorized",status= 401)
	
	currRoom = None

	try:
		currRoom = Room.objects.get(roomID=ID)
	except:
		return HttpResponse("Room Not Found",status= 404)

	if currRoom.occupied:
		return HttpResponse("Room already occupied", status=409)
	else:
		# modify current room to occupied = True and update current datetime
		# modify current room to occupied = True and update current datetime
		currRoom.occupied = True
		currRoom.lastEntered = datetime.now()
		log(ID,1) # We need to uncomment this once stat app models and views are finished
			
		# save changes made to current room (to database)
		currRoom.save()
			
		# create the dictionary of rooms needed to update webpage
	
		return HttpResponse("Room successfully entered!")

@api_view(['POST'])
def exitRoom(request, floor, ID):
	'''
	This function is called when someone exits a room
	@modifies Room object with matching ID
	@return Response to server
	'''
	
	data = request.data

	username = ''
	password = ''

	try:
		username = data['username']
		password = data['password']
	except:
		return HttpResponse("Please supply username and password in body",status= 401)

	#use post data information
	user = authenticate(username=username, password=password)

	if user is not None:
		pass
		# Continue execution
	else:
		return HttpResponse("Unauthorized",status= 401)
	
	currRoom = None

	try:
		currRoom = Room.objects.get(roomID=ID)
	except:
		return HttpResponse("Room Not Found",status= 404)

	if not currRoom.occupied:
		return HttpResponse("Room already empty", status=409)

	currRoom.occupied = False
	currRoom.lastExited = datetime.now()
	log(ID,0) #uncomment when stats log is implemeted
	# save changes made to current room (to database)
	currRoom.save()
	return HttpResponse("Room successfully exited!")
	
