from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Day, Month, Year, StatsLog
from .serializers import DaySerializer, MonthSerializer, YearSerializer
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

class daysView(viewsets.ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer

class monthsView(viewsets.ModelViewSet):
    queryset = Month.objects.all()
    serializer_class = MonthSerializer

class yearsView(viewsets.ModelViewSet):
    queryset = Year.objects.all()
    serializer_class = YearSerializer

"""
@params - 
    * floor: The floor that the room is on (floor3 or floor4)
    * ID: The number of the room (365, 415, etc.)
    * month: The month for which the days info is returned (Jan, Feb, ..., Dec)
@returns - JSON data for all days in the database with matching dates and roomID's
"""
@api_view(['GET'])
def getDaysInfo(ID, month):
    queryset = Day.objects.get(date = month, roomID = ID)
    serializer_class = DaySerializer
    return Response(serializer_class.data)

"""
@params - 
    * floor: The floor that the room is on
    * ID: The number of the room
    * year: The year for which the months info is returned (2000, 2016, 2020, etc.)
@returns - JSON data for all months in the database with matching dates and roomID's
"""
@api_view(['GET'])
def getMonthsInfo(ID, year):
    queryset = Month.objects.get(date = year, roomID = ID)
    serializer_class = MonthSerializer
    return Response(serializer_class.data)

"""
@params - 
    * floor: The floor that the room is on
    * ID: The number of the room
@returns - JSON data for all years in the database with matching roomID's

NOTE: Maybe it would be better if we made it so that the user decides a range of years to get that stats for because 
making it so that it returns ALL the data for EVERY year would be a little much
"""
@api_view(['GET'])
def getYearsInfo(ID):
    queryset = Year.objects.get(roomID = ID)
    serializer_class = YearSerializer
    return Response(serializer_class.data)

def log(rID, e):
	currLog = StatsLog(event = e, roomID = rID, date = datetime.now())
	currLog.save()
