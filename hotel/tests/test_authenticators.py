import pytest
from unittest.mock import patch, Mock
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import AuthenticationFailed

from hotel.authenticators import ManagerKeyAuthenticator


@pytest.mark.django_db
class ManagerKeyAuthenticatorTestCase(TestCase):
    TEST_DATA = {
        'MANAGER_VASYL_KEY': {
            'key': '123456',
            'username': 'vasyl_petrenko',
        },
        'MANAGER_PETRO_KEY': {
            'key': 'aqwsderf',
            'username': 'petro_vasylenko',
        },
    }

    def setUp(self):
        self.env_get_patch = patch('os.environ.get')
        self.env_get = self.env_get_patch.start()
        self.env_get.side_effect = \
            lambda k: self.TEST_DATA.get(k) and self.TEST_DATA[k]['key']

    def tearDown(self):
        self.env_get_patch.stop()

    def test_authenticate_credentials(self):
        for _, v in self.TEST_DATA.items():
            self.assertEqual(
                v['username'],
                ManagerKeyAuthenticator.authenticate_credentials(v['key'])
            )
        self.assertEqual(
            None,
            ManagerKeyAuthenticator.authenticate_credentials('Fake')
        )

    def test_extract_key(self):
        request = Mock()
        request.META = Mock()
        request.META.get = Mock()
        key = 'test_key'
        request.META.get.return_value = key
        self.assertEqual(key, ManagerKeyAuthenticator.extract_key(request))

    def test_authenticate(self):
        manager = self.TEST_DATA['MANAGER_VASYL_KEY']
        key = manager['key']
        user = User.objects.create_user(manager['username'])
        request = Mock()
        request.META = Mock()
        request.META.get = Mock()
        request.META.get.return_value = key
        auth_user, _ = ManagerKeyAuthenticator().authenticate(request)
        self.assertEqual(user, auth_user)
        request.META.get.return_value = None
        auth_user, _ = ManagerKeyAuthenticator().authenticate(request)
        self.assertEqual(None, auth_user)
        request.META.get.return_value = 'Fake'
        self.assertRaises(
            AuthenticationFailed,
            ManagerKeyAuthenticator().authenticate,
            request
        )
