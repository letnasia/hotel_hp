from rest_framework import serializers

from hotel.models import MenuItemCat


class MenuItemCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemCat
        fields = ('id', 'name')
