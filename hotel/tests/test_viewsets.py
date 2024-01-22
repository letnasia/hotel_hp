import datetime as dt
from unittest.mock import patch, Mock

import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from hotel.models import Guest


@pytest.mark.django_db
class GuestTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', password='123456')
        self.guest = Guest.objects.create(
            user=self.user,
            first_name='test',
            last_name='user',
            phone_number='093773867234',
        )

    def test_register(self):
        response = self.client.post(
            '/api/hotel/guest/register',
            content_type='application/json',
            data={
                'login': 'user1',
                'password': 'test12345',
                'first_name': 'vasyl',
                'last_name': 'petrenko',
                'phone_number': '380501234567',
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(
            '/api/hotel/guest/login',
            content_type='application/json',
            data={'login': 'test', 'password': '123456'}
        )
        self.assertEqual(response.status_code, 200)

