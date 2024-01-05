from django.db import models

from hotel.models.role import Role
from hotel.models.shift import Shift


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)
    shifts = models.ManyToManyField(Shift)
