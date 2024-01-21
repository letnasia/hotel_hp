import os
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions


class ManagerKeyAuthenticator(authentication.BaseAuthentication):
    def authenticate(self, request):
        key = self.extract_key(request)

        if not key:
            return None, None

        username = self.authenticate_credentials(key)

        if not username:
            raise exceptions.AuthenticationFailed('Invalid secret key')

        user = User.objects.get(username=username)
        return user, None

    @staticmethod
    def authenticate_credentials(key):
        if key == os.environ.get('MANAGER_VASYL_KEY'):
            return 'vasyl_petrenko'
        if key == os.environ.get('MANAGER_PETRO_KEY'):
            return 'petro_vasylenko'
        return None

    @staticmethod
    def extract_key(request):
        return request.META.get('HTTP_X_MANAGER_KEY')
