import logging

from app.errors import ValidationError

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.validators import (
    UserCreateSerializer,
    AuthCustomTokenSerializer
)
from accounts.services import AccountToolkit, UserCreator


logger = logging.getLogger(__name__)


@api_view(["POST"])
def token_auth_api(request, *args, **kwargs):
    try:
        user, token = AccountToolkit.authenticate(data=request.data)
    except ValidationError as exc:
        logger.exception("A validation error occured during account authorization")
        return Response({"error": str(exc)}, status=400)

    logger.info(f"The user with an email - {user.email} just logged in")
    return Response({
        'token': token.key,
        'user_id': user.id,
        'email': user.email,
        'admin': user.is_admin,
    }, status=200)


@api_view(["POST"])
def create_account_api(request, *args, **kwargs):
    try:
        user = UserCreator(data=request.data)()
    except ValidationError as exc:
        logger.exception("A validation error occured during account creation")
        return Response({"error": str(exc)}, status=400)

    token = AccountToolkit.get_or_create_token(user=user)

    logger.info(f"New account with email - {user.email} is created")
    return Response({
        'token': token.key,
        'user_id': user.id,
        'email': user.email,
        'admin': user.is_admin,
    }, status=201)
