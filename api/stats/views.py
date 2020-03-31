from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import Day, Month, Year

# Create your views here.

"""
@params - 
    * floor: The floor that the room is on (floor3 or floor4)
    * ID: The number of the room (365, 415, etc.)
    * month: The month for which the days info is returned (Jan, Feb, ..., Dec)
@returns - A list of occupancy stats for a given room on each day of a given month
"""
def getDaysInfo(floor, ID, month):
    return

"""
@params - 
    * floor: The floor that the room is on
    * ID: The number of the room
    * year: The year for which the months info is returned (2000, 2016, 2020, etc.)
@returns - A list of occupancy stats for a given room on each day of a given month
"""
def getMonthsInfo(floor, ID, year):
    return

"""
@params - 
    * floor: The floor that the room is on
    * ID: The number of the room
@returns - A list of occupancy stats for a given room for every year

NOTE: Maybe it would be better if we made it so that the user decides a range of years to get that stats for because 
making it so that it returns ALL the data for EVERY year would be a little much
"""
def getYearsInfo(floor, ID):
    return