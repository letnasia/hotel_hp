from django.db import models
import datetime as dt

from hotel.models.guest import Guest
from hotel.models.room import Room


class Reservation(models.Model):
    guest = models.ForeignKey(Guest, related_name='reservations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=dt.datetime.now)
    is_paid = models.BooleanField(default=False)
    pay_deadline = models.DateTimeField()
    end_date = models.DateField()
    rooms = models.ManyToManyField(Room, through='RoomReserve', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['end_date'])
        ]


class RoomReserve(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('date', 'room')
    