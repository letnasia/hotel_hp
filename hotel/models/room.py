from django.db import models

from hotel.models.floor import Floor


class Room(models.Model):
    floor_id = models.ForeignKey(Floor, on_delete=models.RESTRICT)
    size = models.IntegerField()
    accommodation = models.IntegerField()
    description = models.TextField(blank=True)

