import jwt
from django.contrib.auth.models import User
from django.conf import settings

class JWTAuthenticationBackend(object):
    def authenticate(self, request, token=None):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(username=payload['username'])
            return user
        except (jwt.DecodeError, User.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
