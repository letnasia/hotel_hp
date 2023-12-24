from rest_framework import serializers

from hotel.models import Shift


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ('id', 'date', 'number')
