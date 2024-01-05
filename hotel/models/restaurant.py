from django.db import models

from hotel.models.floor import Floor
from hotel.models.menu_item import MenuItem


class Restaurant(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    menu = models.ManyToManyField(MenuItem)
