from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_auth.mixins import AlreadyAuthenticatedMixin
from custom_auth.models import Profile
from custom_auth.serializers import (
    SignUpSerializer,
    SignInSerializer,
    ProfileSerializer,
    UpdateUserSerializer
)


class SignUpAPIView(AlreadyAuthenticatedMixin, CreateAPIView):
    """Create new user"""

    serializer_class = SignUpSerializer


class SignInAPIView(AlreadyAuthenticatedMixin, APIView):
    """Sign in"""

    @extend_schema(
        responses={200: SignInSerializer}
    )
    def post(self, request):
        serializer = SignInSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class SignOutAPIView(LoginRequiredMixin, APIView):
    """Sign out"""

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileAPIView(LoginRequiredMixin, APIView):
    @extend_schema(
        responses={200: ProfileSerializer}
    )
    def get(self, request):
        """Get user profile"""

        user = request.user
        profile = get_object_or_404(Profile, user_id=user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @extend_schema(
        responses={200: UpdateUserSerializer}
    )
    def post(self, request):
        """Update user profile """

        user = request.user

        serializer = UpdateUserSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
