from django.core.validators import MinValueValidator
from django.db import models

from hotel.models.floor import Floor


class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.RESTRICT)
    size = models.IntegerField()
    accommodation = models.IntegerField()
    description = models.TextField(blank=True)
    price = models.FloatField(validators=[MinValueValidator(500)], blank=False)

