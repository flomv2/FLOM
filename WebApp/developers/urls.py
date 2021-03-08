from django.urls import path
from . import views

'''
index - This will find the corresponding view named "index"
	- floor argument passed in to function ('3' or '4')
enterRoom - This will find the corresponding view named "enterRoom"
	- floor ('3' or '4')
	- ID (room ID)
	- Password (password for RasberryPi device)
exitRoom - This will find the correspoding view named "exitRoom"
	- floor ('3' or '4')
	- ID (room ID)
	- Password (password for RasberryPi device)
'''
urlpatterns = [
	path("<floor>", views.index, name="index"),
	path("enter/<floor>/<ID>/<password>", views.enterRoom, name = "enterRoom"),
	path("exit/<floor>/<ID>/<password>", views.exitRoom, name= "exitRoom")
]

# initalize database with data from config.ini file
# ONLY CALLED ONCE AT SERVER STARTUP
views.populateFloors()