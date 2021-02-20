from app.errors import ValidationError

from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .utils import AccountErrorMessages
from .utils import new_password_is_correct


User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):
        if len(value) > 100:
            raise ValidationError(AccountErrorMessages.TOO_LONG_EMAIL_ERROR.value)

        qs = User.objects.filter(email=value)
        if qs.exists():
            raise ValidationError(AccountErrorMessages.NON_UNIQUE_EMAIL_ERROR.value)
        return value

    def validate_password(self, value):
        if not new_password_is_correct(value):
            raise ValidationError(AccountErrorMessages.INCORRECT_PASSWORD_SCHEME_ERROR.value)
        return value 


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            email = email.lower()
            user = authenticate(username=email, password=password)

            if user:
                if not user.is_active:
                    raise ValidationError(AccountErrorMessages.DISABLED_ACCOUNT_ERROR.value)
            else:
                raise ValidationError(AccountErrorMessages.CREDENTIALS_ERROR.value)
        else:
            raise ValidationError(AccountErrorMessages.REQUEST_FIELDS_ERROR.value)

        attrs['user'] = user
        return attrs
