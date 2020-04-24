from rest_framework import serializers
from stats.models import StatsLog, Day, Month, Year

class StatsLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatsLog
        fields = ['event', 'roomID', 'date']

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['roomID', 'date', 'totalOccupants', 'avgOccLength']

class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = ['roomID', 'date', 'totalOccupants', 'avgOccLength']

class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ['roomID', 'date', 'totalOccupants', 'avgOccLength']