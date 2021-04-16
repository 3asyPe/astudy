import logging

from rest_framework.authtoken.models import Token

from accounts.api.validators import UserCreateSerializer
from accounts.models import User
from app.errors import ValidationError


logger = logging.getLogger(__name__)


class UserCreator:
    def __init__(self, data: dict) -> User:
        self.data = data

    def __call__(self) -> User:
        if self.allowed_to_create():
            user =  self._create()
            self._after_creation(user)
            return user
        raise ValidationError()

    def _create(self) -> User:
        email = self.data["email"].lower()
        return User.objects.create(email=email, password=self.data["password"])
    
    def allowed_to_create(self) -> bool:
        validator = UserCreateSerializer(data=self.data)
        return validator.is_valid(raise_exception=True)

    def _after_creation(self, user) -> None:
        Token.objects.get_or_create(user=user)
