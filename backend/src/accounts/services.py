from rest_framework.authtoken.models import Token

from .models import User


def create_user(*, email: str, password: str) -> User:
    user = User.objects.create_user(email=email, password=password)
    return user


def get_or_creat_token(*, user: User) -> Token:
    token, created = Token.objects.get_or_create(user=user)
    return token
