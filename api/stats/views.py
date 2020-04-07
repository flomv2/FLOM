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
@returns - A list of occupancy stats for a given room on each day of a given month in the form [date, totalOccupants, avgOccLength]
"""
def getDaysInfo(floor, ID, month):
    daysInfo = []
    tempData = []
    m = month.date.month
    y = datetime.now().year

    start = datetime.datetime(y, m, 1)
    end = datetime.datetime(y, m+1, 1)
    delta = timedelta(days = 1)
    totalDays = (end - start).days
    days = [start + k * delta for k in range(totalDays)]

    for day in totalDays:
        tempData = []
        temp = Day.objects.get(date = day, roomID = ID)

        tempData.append(temp.date)
        tempData.append(temp.totalOccupants)
        tempData.append(temp.abgOccLength)

        daysInfo.append(tempData)

    return HttpResponse("getDaysInfo() not yet implemented", status = 404)

"""
@params - 
    * floor: The floor that the room is on
    * ID: The number of the room
    * year: The year for which the months info is returned (2000, 2016, 2020, etc.)
@returns - A list of occupancy stats for a given room during each month of a given year in the form [date, totalOccupants, avgOccLength]
"""
def getMonthsInfo(floor, ID, year):
    monthsInfo = []
    tempData = []
    y = year.date.year
    for i in range(13):
        tempData = []
        m = datetime.datetime(y, i, 1)
        month = Month.objects.get(date = m, roomID = ID)

        tempData.append(month.date)
        tempData.append(month.totalOccupants)
        tempData.append(month.avgOccLength)

        monthsInfo.append(tempData)

    return HttpResponse("getMonthsInfo() not yet implemented", status = 404)

"""
@params - 
    * floor: The floor that the room is on
    * ID: The number of the room
@returns - A list of occupancy stats for a given room for every year in the form [date, totalOccupants, avgOccLength]

NOTE: Maybe it would be better if we made it so that the user decides a range of years to get that stats for because 
making it so that it returns ALL the data for EVERY year would be a little much
"""
def getYearsInfo(floor, ID):
    return HttpResponse("getYearsInfo() not yet implemented", status = 404)