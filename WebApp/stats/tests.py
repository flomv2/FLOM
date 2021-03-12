from django.test import TestCase
#import datetime
from .models import *
from .views import *
from datetime import datetime as dt
import pytz

class RoomUsageModelTest(TestCase):

# 	def testDefaultValues(self) {
# 		'''
# 		Tests the RoomUsage model with defualt values
# 		'''
# 		room = Room(roomID = '302-A', occupied = False, lastEntered = datetime.now(), lastExited = datetime.now(), roomType = 'Group')
# 		occupancy = OccupancyStats(totalOccupancy = 0)
# 		roomUsage = RoomUsage(room = room, occupancyStats = occupancy, currentDate = datetime.now())
# 		# test string representation of models
# 		self.assertEqual(str(room), 'Room: ' + roomUsage.room.roomID)
# 		self.assertEqual(str(occupancy), 'Total Occupancy: ' + str(roomUsage.occupancyStats.totalOccupancy))
# 		self.assertEqual(str(roomUsage), 'Usage for ' + roomUsage.room.roomID)
# 		# test default total occupancy
# 		self.assertEqual(roomUsage.occupancyStats.totalOccupancy, 0)
# 	}
	@classmethod
	def setUpTestData(cls):
		print("SET UP")
		# assert(False == True)
		# print(beforeLog1.timeStamp)
		# day301 = createTimeObject(301, "day", now)
		# month301 = createTimeObject(301, "month", now)
		# year301 = createTimeObject(301, "year", now)
		# day302 = createTimeObject(302, "day", now)
		# month302 = createTimeObject(302, "month", now)
		# year302 = createTimeObject(302, "year", now)

	#test logs are saved properly
	@classmethod
	def testLog(self):
		d1 = dt(2019, 11, 15, 2, 35, 2)
		print("ORIGINAL: ",d1)
		#Creates test events that occurr
		log1 = StatsLog(event = 1, roomID = "311", date = d1)
		log1.save()
		d2 = dt(2019, 11, 15, 2, 40, 3)
		log2 = StatsLog(event = 0, roomID = "311", date = d2)
		log2.save()
		d3 = dt(2019, 11, 15, 3, 30, 4)
		log3 = StatsLog(event = 1, roomID = "311", date = d3)
		log3.save()
		d4 = dt(2019, 11, 15, 4, 37, 23)
		log4 = StatsLog(event = 0, roomID = "311", date = d4)
		log4.save()
		timeObject = Day()
		timeObject.roomID = "311"
		#datetime(Year Month Day Hour Minute Seconds)
		timenow = dt(2019, 11, 15, 5, 37, 23)
		#Creates the test day to create statistics for
		timeObject.date = timenow
		duration = "day"
		logList = importLog("311", timenow, duration)
		#Calculates the statistics for that day and then saves
		timeObject.totalOccupants = getOccupants(logList, duration)
		timeObject.avgOccLength = calcAvgOccLength(logList, duration)
		timeObject.save()