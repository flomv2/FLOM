from rest_framework import serializers
from floor.models import Floor, Room



class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['name','roomCount']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['roomID', 'occupied', 'lastExited','lastEntered','roomType','floor']