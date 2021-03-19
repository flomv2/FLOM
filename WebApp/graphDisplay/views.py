from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StatsLogSerializer, DaySerializer, MonthSerializer, YearSerializer
from stats.models import StatsLog, Day,  Month, Year
# Create your views here.

class StatsLogView(viewsets.ModelViewSet):
    serializer_class = StatsLogSerializer
    queryset = StatsLog.objects.all()

class DayView(viewsets.ModelViewSet):
    serializer_class = DaySerializer
    queryset = Day.objects.all()
    
#Fill in rest here