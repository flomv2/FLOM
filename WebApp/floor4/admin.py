from django.contrib import admin

from floor4.models import Room

class RoomAdmin(admin.ModelAdmin):
	list_display = ('roomID', 'occupied', 'lastEntered', 'lastExited')
admin.site.register(Room, RoomAdmin)

# Register your models here.