import datetime as dt
from unittest.mock import patch
import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.test import TestCase

from hotel.exceptions import DateFromPast, ReserveLimit, RoomNotFound, \
    RoomAlreadyReserved
from hotel.models import Floor, Room, Reservation, RoomReserve, Guest
from hotel.serializers.reservation import ReservationViewSerializer, \
    ReservationSerializer
from hotel.serializers.room import RoomSerializer


@pytest.mark.django_db
class ReservationSerializerCase(TestCase):
    def setUp(self):
        self.floor = Floor.objects.create(level=1)
        room_data = [
            {
                "floor": self.floor,
                "size": 20,
                "accommodation": 2,
                "price": 1200,
            },
            {
                "floor": self.floor,
                "size": 16,
                "accommodation": 1,
                "price": 800,
            },
            {
                "floor": self.floor,
                "size": 32,
                "accommodation": 3,
                "price": 2000,
            },
        ]

        self.rooms = [
            Room.objects.create(**args)
            for args in room_data
        ]

        self.user = User.objects.create_user('test')
        self.guest = Guest.objects.create(
            user=self.user,
            first_name='test',
            last_name='user',
            phone_number='093773867234',
        )
        self.start_date = dt.date.today() + dt.timedelta(days=5)
        self.end_date = self.start_date + dt.timedelta(days=10)
        dates = [
            self.start_date + dt.timedelta(i)
            for i in range((self.end_date - self.start_date).days + 1)
        ]
        with transaction.atomic():
            self.reservation = Reservation.objects.create(
                guest=self.guest,
                pay_deadline=dt.datetime.now() + dt.timedelta(days=2),
                end_date=self.end_date,
            )
            reserves = [
                RoomReserve(
                    reservation_id=self.reservation.id,
                    room_id=room.id,
                    date=date,
                )
                for room in self.rooms
                for date in dates
            ]
            RoomReserve.objects.bulk_create(reserves)

    def tearDown(self):
        pass

    def test_get_rooms(self):
        serializer = ReservationViewSerializer()
        expected = [
            RoomSerializer(room).data
            for room in self.rooms
        ]
        self.assertEqual(expected, serializer.get_rooms(self.reservation))

    def test_get_start_date(self):
        serializer = ReservationViewSerializer()
        self.assertEqual(
            self.start_date,
            serializer.get_start_date(self.reservation)
        )

    def test_create_from_past(self):
        start_date = dt.date.today() - dt.timedelta(days=1)
        end_date = start_date + dt.timedelta(days=10)
        data = {
            'user': self.user,
            'rooms': [room.id for room in self.rooms],
            'start_date': start_date,
            'end_date': end_date,
        }
        serializer = ReservationSerializer()
        self.assertRaises(
            DateFromPast,
            serializer.create,
            data
        )

    def test_create_limit(self):
        start_date = dt.date.today() + dt.timedelta(days=5)
        end_date = start_date + dt.timedelta(
            days=ReservationSerializer.RESERVE_LIMIT_DAYS + 1
        )
        data = {
            'user': self.user,
            'rooms': [room.id for room in self.rooms],
            'start_date': start_date,
            'end_date': end_date,
        }
        serializer = ReservationSerializer()
        self.assertRaises(
            ReserveLimit,
            serializer.create,
            data
        )

    def test_create_no_room(self):
        start_date = dt.date.today() + dt.timedelta(days=5)
        end_date = start_date + dt.timedelta(days=10)
        data = {
            'user': self.user,
            'rooms': [room.id for room in self.rooms] + [12345],
            'start_date': start_date,
            'end_date': end_date,
        }
        serializer = ReservationSerializer()
        self.assertRaises(
            RoomNotFound,
            serializer.create,
            data
        )

    def test_create_already_reserved(self):
        start_date = self.end_date
        end_date = start_date + dt.timedelta(days=10)
        data = {
            'user': self.user,
            'rooms': [room.id for room in self.rooms],
            'start_date': start_date,
            'end_date': end_date,
        }
        serializer = ReservationSerializer()
        self.assertRaises(
            RoomAlreadyReserved,
            serializer.create,
            data
        )

    def test_to_representation(self):
        expected = ReservationViewSerializer(self.reservation).data
        serializer = ReservationSerializer()
        self.assertEqual(
            expected,
            serializer.to_representation(self.reservation)
        )

    def test_get_pay_deadline(self):
        serializer = ReservationSerializer(self.reservation)
        now = dt.datetime.now()
        deadline = serializer.get_pay_deadline(dt.date.today())
        self.assertGreaterEqual(dt.timedelta(hours=2), deadline - now)
        self.assertLessEqual(dt.timedelta(hours=1), deadline - now)

    @patch('hotel.tasks.reservation_created.apply_async')
    def test_create(self, hook_task):
        start_date = dt.date.today() + dt.timedelta(days=25)
        end_date = start_date + dt.timedelta(days=10)
        data = {
            'user': self.user,
            'rooms': [room.id for room in self.rooms],
            'start_date': start_date,
            'end_date': end_date,
        }
        serializer = ReservationSerializer()
        reservation = serializer.create(data)
        hook_task.return_value = ''
        hook_task.assert_called_once_with(
            args=(reservation.id,)
        )

