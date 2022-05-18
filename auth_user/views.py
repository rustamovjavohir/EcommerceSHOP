from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_tor_users(user):
    refresh = RefreshToken.for_user(user=user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }



