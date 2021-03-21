from django.shortcuts import render
from stats.models import StatsLog, Day,  Month, Year
from django.http import HttpResponse
from datetime import datetime
from django.core.cache import cache
import time
import datetime
import threading
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from floor.models import Room
from django.db.models import Sum, Avg, F 
from django.contrib.auth.decorators import login_required
from .forms import RoomRequestForm

def get_stats(ID):
	stats = {}
	stats['day'] = Day.objects.filter(roomID=ID)
	stats['month'] = Month.objects.filter(roomID=ID)
	stats['year'] = Year.objects.filter(roomID=ID)
	stats['ID'] = ID
	return stats

def createGraph(stats, duration=''):
	# remove old graphs
	if os.path.exists('stats/static/days.png') and duration == 'day':
		os.remove('stats/static/days.png')
	if os.path.exists('stats/static/months.png') and duration == 'month':
		os.remove('stats/static/months.png')
	if os.path.exists('stats/static/years.png') and duration == 'year':
		os.remove('stats/static/years.png')
	x = []
	y = []
	z = []
	for obj in stats:
		x.append(obj.date)
		y.append(obj.totalOccupants)
		z.append(obj.avgOccLength.total_seconds()/60.0)
	fig, (ax1, ax2) = plt.subplots(1, 2)
	plt.subplots_adjust(left=.125, right=.9, bottom=.1, top=.9, wspace=.2, hspace=.2)
	ax1.bar(x, y, align='center', alpha=0.5)
	ax2.bar(x, z, align='center', alpha=0.5)
	fig.autofmt_xdate()
	fig.set_figheight(10)
	fig.set_figwidth(15)
	ax1.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
	ax2.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
	ax1.set_xlabel('Date')
	ax2.set_xlabel('Date')
	ax1.set_ylabel('Total Occupants')
	ax2.set_ylabel('Average Occupancy Time (minutes)')
	if duration == 'day':
		fig.suptitle('Total Occupants & Average Occupancy Time for Days')
		plt.savefig('stats/static/days.png')
	elif duration == 'month':
		fig.suptitle('Total Occupants & Average Occupancy Time for Months')
		plt.savefig('stats/static/months.png')
	elif duration == 'year':
		fig.suptitle('Total Occupants & Average Occupancy Time for Years')
		plt.savefig('stats/static/years.png')
	plt.close()

@login_required
def index(request):
	'''
	@return display of stats page
	'''
	if request.method == 'POST':
		form = RoomRequestForm(request.POST)
		if form.is_valid():
			stats = get_stats(form.data['room'])
			# create and save new graphs
			createGraph(stats['day'], duration='day')
			createGraph(stats['month'], duration='month')
			createGraph(stats['year'], duration='year')
			return render(request, 'stats/templates/html/stats.html', {'stats':stats})
	else:
		form = RoomRequestForm()
	return render(request, 'stats/templates/html/stats.html', {'form': form})

def log(rID, e):
	currLog = StatsLog(event = e, roomID = rID, date = datetime.datetime.now())
	currLog.save()


def createTimeObject(ID, duration, now):
	timeObject = None
	if duration == "day":
		timeObject = Day()
	elif duration == "month":
		timeObject = Month()
	elif duration == "year":
		timeObject = Year()
	else:
		print("ERROR: INVALID TIME OBJECT REQUEST")
	timeObject.date = now
	timeObject.roomID = ID
	logList = importLog(ID, now, duration)
	timeObject.totalOccupants = getOccupants(logList, duration)
	timeObject.avgOccLength = calcAvgOccLength(logList, duration)
	timeObject.save()


def threadf(name):
	'''
	Seperate thread which creates time objects
	every hour/day/month/year. Everytime one of 
	those pass create an object with information
	from logs for each room 
	'''
	start = datetime.datetime.now()
	last = start

	floor3IDs = cache.get('floor3')
	floor4IDs = cache.get('floor4')
	now = datetime.datetime.now()
	while True:
		time.sleep(5)
		now = datetime.datetime.now()
		entered = False
		if now.day != last.day:
			for ID in floor3IDs:
				createTimeObject(ID,"day", last)
			for ID in floor4IDs:
				createTimeObject(ID,"day", last)
			entered = True
		if now.month != last.month:
			for ID in floor3IDs:
				createTimeObject(ID,"month", last)				
			for ID in floor4IDs:
				createTimeObject(ID,"month", last)
			entered = True
		if now.year != last.year:
			for ID in floor3IDs:
				createTimeObject(ID,"year", last)
			for ID in floor4IDs:
				createTimeObject(ID,"year", last)
			entered = True
		if entered:
			last = now


def startThread():
	print("Starting Thread")
	t = threading.Thread(target=threadf, args=(1,))
	t.setDaemon(True)
	t.start()

def importLog(ID, now, duration):	
	query = None
	if duration == 'day':
		query = StatsLog.objects.filter(roomID=ID,date__month=now.month, date__day=now.day)
	elif duration == 'month':
		query = Day.objects.filter(roomID=ID, date__year=now.year, date__month=now.month)
	elif duration == 'year':
		query = Month.objects.filter(roomID=ID, date__year=now.year)
	return query


def getOccupants(query, duration):
	'''
	Return the number of people in the room.
	Gets information from logs.
	'''
	if duration == 'day':
		return int(len(query)/2)
	elif duration == 'month':
		return int(query.aggregate(Sum(F('totalOccupants'))))
	elif duration == 'year':
		return int(query.aggregate(Sum(F('totalOccupants'))))
	return 0

def calcTimeDifference(query):
	timeDiff = []
	tmp_entry = None
	for log in query:
		# if the log contains entry data
		if log.event == 1:
			tmp_entry = log
		# else the log contains exit data
		else:
			timeDiff.append(log.date - tmp_entry.date)
	return timeDiff

def calcAvgOccLength(query, duration):
	'''
	Return the average amount of time
	the room has spent occupied. 
	Gets information from logs.
	'''
	if duration == 'day':
		timeDiff = calcTimeDifference(query)
		if len(timeDiff) != 0:
			return sum(timeDiff, datetime.timedelta(0)) / len(timeDiff)
		else:
			return 0
	elif duration == 'month':
		return query.aggregate(Avg(F('avgOccLength')))
	elif duration == 'year':
		return query.aggregate(Avg(F('avgOccLength')))
	return None