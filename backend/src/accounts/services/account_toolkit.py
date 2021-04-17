from django.conf import settings
from rest_framework.authtoken.models import Token

from accounts.api.validators import AuthCustomTokenSerializer


User = settings.AUTH_USER_MODEL


class AccountToolkit:
    @classmethod
    def authenticate(cls, data) -> (User, Token):
        serializer = AuthCustomTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = cls.get_or_create_token(user=user)
        return user, token

    @classmethod
    def get_or_create_token(cls, user):
        return Token.objects.get_or_create(user=user)[0]