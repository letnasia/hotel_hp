from rest_framework import serializers

from hotel.models import Floor


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ('id', 'level')
