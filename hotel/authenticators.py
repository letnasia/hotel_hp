import os
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions, HTTP_HEADER_ENCODING


class ManagerKeyAuthenticator(authentication.BaseAuthentication):
    def authenticate(self, request):
        key = self.extract_key(request)

        if not key:
            return None

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
        auth = request.META.get('HTTP_X_MANAGER_KEY', b'')
        if isinstance(auth, str):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)
        return auth
