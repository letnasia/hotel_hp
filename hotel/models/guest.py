from django.db import models
import datetime as dt


class Guest(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    created_at = models.DateTimeField(default=dt.datetime.now)
