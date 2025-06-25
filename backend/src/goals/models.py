from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Area(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#000000")  # código HEX
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="areas")

    def __str__(self):
        return self.name

class Goal(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="goals")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="subgoals")
    start_date = models.DateField()
    end_date = models.DateField()
    level = models.IntegerField(default=0)  # Nivel jerárquico: 0 = objetivo raíz
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")

    def __str__(self):
        return self.title

class ScheduleEntry(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="schedule_entries")
    date = models.DateField()
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedule_entries")

    def __str__(self):
        return f"{self.goal.title} - {self.date}"