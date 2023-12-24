from django.db import models

from hotel.models.menu_item_cat import MenuItemCat


class MenuItem(models.Model):
    category_id = models.ForeignKey(MenuItemCat, on_delete=models.RESTRICT)
    price = models.FloatField()
    description = models.TextField(blank=True)