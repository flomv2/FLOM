from django.db import models

class Floor(models.Model):
	'''
	This floor model is used to represent both floor 3 and floor 4
	@member (s)
		floor - 'floor3' or 'floor4'
	'''
	name = models.CharField(max_length=6)
	roomCount = models.IntegerField(default=0)

class Room(models.Model):
	'''
	Model for a Room
	@member (s)
		roomID - the number of the room (ex. 301, 324)
		occupied - occupation status of the room (0 = false, 1 = true)
		lastExited - date of last exit
		lastEntered - date of last entry
		roomType - group or single room
		floor - points to the floor that the room belongs to
	'''
	roomID = models.CharField(max_length = 5) # ID of room (Ex. 301, 324)
	occupied = models.IntegerField() # 0 for empty, 1 for occupied
	lastExited = models.DateField()
	lastEntered = models.DateField()
	roomType = models.CharField(max_length=6, default='S') #single/group for now, could get more descriptive potentially
	floor = models.ForeignKey(Floor, on_delete=models.CASCADE) # room gets mapped to a floor
