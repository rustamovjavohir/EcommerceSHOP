from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
    TokenObtainSlidingView, TokenRefreshSlidingView
)
from .views import SingUpView, BlacklistRefreshView

urlpatterns = [
    path('signup/', SingUpView.as_view(), name='sign_up'),
    # path('api/logout/', BlacklistRefreshView.as_view(), name="logout"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
