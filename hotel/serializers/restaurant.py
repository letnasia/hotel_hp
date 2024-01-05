from rest_framework import serializers

from hotel.models import Restaurant
from hotel.serializers.menu_item import MenuItemSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'floor', 'name')


class RestaurantWithMenuSerializer(RestaurantSerializer):
    menu = MenuItemSerializer(many=True)

    class Meta(RestaurantSerializer.Meta):
        fields = RestaurantSerializer.Meta.fields + ('menu',)


class RestaurantMenuItemsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    items = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Restaurant
        fields = ('id', 'items')
