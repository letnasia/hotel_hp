from django.db import models


class Floor(models.Model):
    level = models.IntegerField()