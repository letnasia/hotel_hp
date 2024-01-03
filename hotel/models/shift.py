from django.db import models


class Shift(models.Model):
    date = models.DateField()
    number = models.IntegerField()

    class Meta:
        unique_together = ('date', 'number')
