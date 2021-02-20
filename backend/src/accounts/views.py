from app.errors import ValidationError

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    UserCreateSerializer,
    AuthCustomTokenSerializer
)
from .services import (
    create_user,
    get_or_creat_token,
)


@api_view(["POST"])
def token_auth_api(request, *args, **kwargs):
    serializer = AuthCustomTokenSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as exc:
        return Response({"error": str(exc)}, status=400)
    
    user = serializer.validated_data['user']
    token = get_or_creat_token(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'email': user.email,
        'admin': user.is_admin,
    }, status=200)


@api_view(["POST"])
def create_account_api(request, *args, **kwargs):
    serializer = UserCreateSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as exc:
        return Response({"error": str(exc)}, status=400)

    user = create_user(**serializer.validated_data)
    token = get_or_creat_token(user=user)

    return Response({
        'token': token.key,
        'user_id': user.id,
        'email': user.email,
        'admin': user.is_admin,
    }, status=201)
