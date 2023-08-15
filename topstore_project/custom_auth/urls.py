from django.urls import path

from custom_auth.views import (
    SignUpAPIView,
    SignInAPIView,
    SignOutAPIView, ProfileAPIView,
)

app_name = 'custom_auth'


urlpatterns = [
    path('sign-up/', SignUpAPIView.as_view(), name='sign-up'),
    path('sign-in/', SignInAPIView.as_view(), name='sign-in'),
    path('sign-out/', SignOutAPIView.as_view(), name='sign-out'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
