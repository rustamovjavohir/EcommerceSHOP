from django.db import transaction
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserSerializers


def get_tokens_tor_users(user):
    refresh = RefreshToken.for_user(user=user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class SingUpView(CreateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()

    @transaction.atomic
    @swagger_auto_schema(operation_summary="Ro'yhatdan o'tish")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response("Success", status=status.HTTP_200_OK)

