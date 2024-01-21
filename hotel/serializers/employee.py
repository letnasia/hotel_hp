# pylint: disable=abstract-method
from rest_framework import serializers

from hotel.models import Employee
from hotel.serializers.shift import ShiftSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'first_name', 'last_name', 'role')


class EmployeeWithShiftsSerializer(EmployeeSerializer):
    shifts = ShiftSerializer(many=True)

    class Meta(EmployeeSerializer.Meta):
        fields = EmployeeSerializer.Meta.fields + ('shifts',)


class EmployeeShiftsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    shifts = serializers.ListField(child=serializers.IntegerField())
