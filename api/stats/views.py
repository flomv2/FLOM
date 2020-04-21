from django.shortcuts import render
from django.http import HttpResponse
from rest_frameowrk import viewsets
from .models import Day, Month, Year
from .serializers import DaySerializer, MonthSerializer, YearSerializer

# Create your views here.

"""
TODO: fix monthsInfo and yearsInfo and test daysInfo to see if it works, which I don't think it does
"""

"""
@params - 
    * floor: The floor that the room is on (floor3 or floor4)
    * ID: The number of the room (365, 415, etc.)
    * month: The month for which the days info is returned (Jan, Feb, ..., Dec)
@returns - A list of occupancy stats for a given room on each day of a given month in the form [date, totalOccupants, avgOccLength]
"""
def getDaysInfo(floor, ID, month, viewsets.ModelViewSet):
    queryset = Day.objects.all()
    serializer_class = DaySerializer

"""
@params - 
    * floor: The floor that the room is on
    * ID: The number of the room
    * year: The year for which the months info is returned (2000, 2016, 2020, etc.)
@returns - A list of occupancy stats for a given room during each month of a given year in the form [date, totalOccupants, avgOccLength]
"""
def getMonthsInfo(floor, ID, year, viewsets.ModelViewSet):
    queryset = Month.objects.all()
    serializer_class = MonthSerializer

"""
@params - 
    * floor: The floor that the room is on
    * ID: The number of the room
@returns - A list of occupancy stats for a given room for the last ten years in the form [date, totalOccupants, avgOccLength]

NOTE: Maybe it would be better if we made it so that the user decides a range of years to get that stats for because 
making it so that it returns ALL the data for EVERY year would be a little much
"""
def getYearsInfo(floor, ID):
    queryset = Year.objetcs.all()
    serializer_class = YearSerializer