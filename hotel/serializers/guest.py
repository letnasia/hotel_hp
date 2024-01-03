from rest_framework import serializers

from hotel.models import Guest


class GuestSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, guest):
        return guest.user.id

    class Meta:
        model = Guest
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'created_at'
        )


class GuestCreateSerializer(serializers.ModelSerializer):
    login = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Guest
        fields = (
            'login',
            'password',
            'first_name',
            'last_name',
            'phone_number'
        )


class GuestLoginSerializer(serializers.ModelSerializer):
    login = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Guest
        fields = (
            'login',
            'password',
        )
