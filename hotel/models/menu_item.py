from django.db import models

from hotel.models.menu_item_cat import MenuItemCat


class MenuItem(models.Model):
    category_id = models.ForeignKey(MenuItemCat, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
