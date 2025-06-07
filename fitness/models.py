from django.db import models
from core.mixins import BaseModel, Timestamps, SoftDelete


class FitnessClass(BaseModel, Timestamps, SoftDelete):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    available_slots = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Booking(BaseModel, Timestamps, SoftDelete):
    fitness_class = models.ForeignKey(
        FitnessClass, on_delete=models.CASCADE, related_name="class_booking", null=True, db_index=True)
    client_name = models.CharField(max_length=100)
    client_email = models.CharField(blank=True, null=True, max_length=50)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
