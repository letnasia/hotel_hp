import datetime as dt
from unittest.mock import patch
import pytest
from django.contrib.auth.models import User
from django.db import transaction
from django.test import TestCase
from django.utils import timezone

from hotel import tasks
from hotel.models import Role, Employee, Shift, Floor, Room, Guest, \
    Reservation, RoomReserve


@pytest.mark.django_db
class CleanupShiftsTestCase(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name='role1')
        self.employee1 = Employee.objects.create(
            first_name='fn1',
            last_name='ln1',
            role=self.role,
        )
        self.employee2 = Employee.objects.create(
            first_name='fn2',
            last_name='ln2',
            role=self.role,
        )
        self.threshold_date = dt.date.today() - dt.timedelta(days=7)

        for i in range(1, 6):
            date = self.threshold_date - dt.timedelta(days=i)
            shift = Shift.objects.create(date=date, number=1)
            self.employee1.shifts.add(shift)
            self.employee2.shifts.add(shift)

        self.retained_shifts1 = []
        self.retained_shifts2 = []

        for i in range(1, 6):
            date = self.threshold_date + dt.timedelta(days=i)
            shift = Shift.objects.create(date=date, number=1)
            self.employee1.shifts.add(shift)
            self.retained_shifts1.append(shift)
            self.employee2.shifts.add(shift)
            self.retained_shifts2.append(shift)

    def tearDown(self):
        Shift.objects.all().delete()

    def test_cleanup_shifts(self):
        tasks.cleanup_shifts()

        self.assertEqual(
            self.retained_shifts1,
            list(self.employee1.shifts.filter(employee=self.employee1))
        )
        self.assertEqual(
            self.retained_shifts2,
            list(Shift.objects.all().filter(employee=self.employee2))
        )


@pytest.mark.django_db
class ReservationTestCase(TestCase):
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
                pay_deadline=timezone.now() + dt.timedelta(days=2),
                end_date=self.end_date,
                created_at=timezone.now() - dt.timedelta(days=1)
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

    @patch('hotel.tasks.send_message')
    def test_reservation_created(self, send_message):
        send_message.return_value = True
        tasks.reservation_created(self.reservation.id)
        message = send_message.call_args.args[0]
        self.assertTrue(isinstance(message,str))
        self.assertTrue(f'New reservation {self.reservation.id}' in message)

    @patch('hotel.tasks.write_to_sheet')
    def test_reservation_daily_stats(self, write_to_sheet):
        write_to_sheet.return_value = True
        tasks.reservation_daily_stats()
        file = write_to_sheet.call_args.args[0]
        rows = write_to_sheet.call_args.args[1]
        self.assertTrue(isinstance(file, str))
        self.assertTrue(len(rows))
