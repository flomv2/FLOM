from django.shortcuts import render
from .models import StatsLog
from datetime import datetime

# Create your views here.
def log(rID, e):
	currLog = StatsLog(event = e, roomID = rID, date = datetime.now())
	currLog.save()
