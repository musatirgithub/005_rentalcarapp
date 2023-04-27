from typing import Collection, Optional
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
GEAR = (
    ('a', 'automatic'),
    ('m', 'manuel')
)


class Car(models.Model):
    plate_number = models.CharField(max_length=15)
    brand = models.CharField(max_length=15)
    model = models.CharField(max_length=15)
    year = models.SmallIntegerField()
    gear = models.CharField(max_length=1, choices=GEAR)
    rent_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField()


class Reservation(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reservations_customer')
    car = models.ForeignKey(Car, on_delete=models.CASCADE,
                            related_name='reservations_car')
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'start_date', 'end_date'], name='user_rent_date'
            )
        ]
