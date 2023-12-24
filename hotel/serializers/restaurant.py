from rest_framework import serializers

from hotel.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('id', 'floor_id', 'name')
