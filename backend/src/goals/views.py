from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Area, Goal, ScheduleEntry
from .serializers import AreaSerializer, GoalSerializer, ScheduleEntrySerializer
from datetime import timedelta, datetime, date
from django.utils import timezone

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Area.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        goal = serializer.save(user=self.request.user)
        subgoals_data = self.request.data.get("subgoals", [])
        self._create_schedule_entries(goal)
        for subgoal_data in subgoals_data:
            self._create_subgoal_recursive(subgoal_data, parent=goal, level=1)

    def _create_subgoal_recursive(self, data, parent, level):
        subgoal = Goal.objects.create(
            title=data["title"],
            description=data.get("description", ""),
            start_date=data["start_date"],
            end_date=data["end_date"],
            area=parent.area,
            parent=parent,
            level=level,
            user=parent.user
        )
        sub_subgoals = data.get("subgoals", [])
        if sub_subgoals and level < 2:  # máximo 3 niveles
            for child in sub_subgoals:
                self._create_subgoal_recursive(child, parent=subgoal, level=level + 1)
        else:
            self._create_schedule_entries(subgoal)

    def _create_schedule_entries(self, goal):
        start = goal.start_date
        end = goal.end_date

        # Si vienen como string (pasa en subgoals creados con .create()), convertimos
        if isinstance(start, str):
            start = datetime.strptime(start, "%Y-%m-%d").date()
        if isinstance(end, str):
            end = datetime.strptime(end, "%Y-%m-%d").date()

        current = start
        while current <= end:
            ScheduleEntry.objects.create(
                goal=goal,
                date=current,
                user=goal.user
            )
            current += timedelta(days=1)

class ScheduleEntryViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return ScheduleEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
