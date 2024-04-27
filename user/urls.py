from django.urls import path
from user.views import RefreshAccessToken, UserRegisterView, UserLoginView, VerifyEmailToken

urlpatterns = [
    path('user-registration/', UserRegisterView.as_view(), name='user'),
    path('user-login/', UserLoginView.as_view(), name='user-login'),
    path('verify-email/', VerifyEmailToken.as_view(), name='verify-email'),
    path('token/refresh/',RefreshAccessToken.as_view(), name='refresh-token'),
]
