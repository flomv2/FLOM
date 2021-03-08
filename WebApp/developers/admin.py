from django.contrib import admin

from .models import Floor, Room

class FloorAdmin(admin.ModelAdmin):
	'''
	Model for displaying info on admin page for Floor model
	'''
	list_display = ('name', 'roomCount')

class RoomAdmin(admin.ModelAdmin):
	'''
	Model for displaying info on admin page for Room model
	'''
	list_display = ('roomID', 'occupied', 'lastExited', 'lastEntered', 'roomType', 'floor')
	
admin.site.register(Floor, FloorAdmin)
admin.site.register(Room, RoomAdmin)