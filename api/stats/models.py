from django.db import models
from datetime import datetime

from floor.models import Room

class StatsLog(models.Model):
	'''
	Contains useful occupancy statistics
	@member (s)
		room - Room for which the logs are stored for
		event - enter/exit-1/0
		roomID = room ID of room
		timeStamp - exact date time of the log
	'''
	event = models.IntegerField(default = 0)
	roomID = models.CharField(max_length = 5)
	#CHANGE THIS BACK TO editable = False AFTER TESTING
	date = models.DateTimeField()

'''
	These models are a representation of the usage statistics that have
	been gathered within the span of the designated time.
	@member (s)
		date - date on which TimeFrame was created
		room - points to the room it refers to
		roomID - individual room this applies to
		totalOccupants - total number of occupants over the span
		avgOccLength - average occupation length for a room (in minutes)
'''
# class Hour(models.Model):
# 	date = models.DateTimeField()
# 	roomID = models.CharField(max_length=5)
# 	totalOccupants = models.IntegerField(default=0)

class Day(models.Model):
	date = models.DateTimeField()
	roomID = models.CharField(max_length=5)
	totalOccupants = models.IntegerField(default=0)
	avgOccLength = models.DurationField()


class Month(models.Model):
	date = models.DateTimeField()
	roomID = models.CharField(max_length=5)
	totalOccupants = models.IntegerField(default=0)
	avgOccLength = models.DurationField()

class Year(models.Model):
	date = models.DateTimeField()
	roomID = models.CharField(max_length=5)
	totalOccupants = models.IntegerField(default=0)
	avgOccLength = models.DurationField()