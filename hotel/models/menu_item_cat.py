from django.db import models


class MenuItemCat(models.Model):
    name = models.CharField(max_length=255)