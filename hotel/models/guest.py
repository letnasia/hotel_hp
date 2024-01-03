from django.contrib.auth.models import User
from django.db import models
import datetime as dt


class Guest(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    created_at = models.DateTimeField(default=dt.datetime.now)
