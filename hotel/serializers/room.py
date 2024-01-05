from rest_framework import serializers

from hotel.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'id',
            'floor',
            'size',
            'accommodation',
            'price',
            'description'
        )
