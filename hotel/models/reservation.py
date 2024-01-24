from django.db import models
from django.utils import timezone

from hotel.models.guest import Guest
from hotel.models.room import Room


class Reservation(models.Model):
    guest = models.ForeignKey(
        Guest,
        related_name='reservations',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    pay_deadline = models.DateTimeField()
    end_date = models.DateField()
    rooms = models.ManyToManyField(Room, through='RoomReserve', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['end_date'])
        ]

    def get_unique_rooms(self):
        reserves = RoomReserve.objects\
            .filter(reservation_id=self.id)\
            .values_list('room_id', flat=True)
        return Room.objects.filter(id__in=reserves)

    def get_start_date(self):
        return RoomReserve.objects.all()\
                .filter(reservation__id=self.id)\
                .order_by('date')[0].date


class RoomReserve(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('date', 'room')
    