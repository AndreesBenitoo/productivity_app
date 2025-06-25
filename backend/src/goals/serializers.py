from rest_framework import serializers
from .models import Area, Goal, ScheduleEntry

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        exclude = ['user']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        exclude = ['user']

class ScheduleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleEntry
        exclude = ['user']