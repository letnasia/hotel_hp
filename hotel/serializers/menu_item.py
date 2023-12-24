from rest_framework import serializers

from hotel.models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'category_id', 'price', 'description')
