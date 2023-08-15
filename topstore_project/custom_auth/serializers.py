from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer

from basket.models import Basket

from custom_auth.models import Profile


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'password'
        ]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.create(
            user=user
        )
        Basket.objects.create(
            user=user
        )

        return user


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return user

        raise serializers.ValidationError(
            'Invalid username/password. Please try again.'
        )


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email')
    phone = serializers.CharField()
    avatar = serializers.ImageField()

    class Meta:
        model = Profile
        fields = [
            'full_name',
            'email',
            'phone',
            'avatar'
        ]

    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'


class UpdateUserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone', required=False)
    avatar = serializers.ImageField(
        source='profile.avatar',
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name',
            instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name',
            instance.last_name
        )
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile_data = validated_data.get('profile')

        if profile_data is not None:
            profile = get_object_or_404(Profile, user_id=instance.id)

            profile.phone = profile_data.get('phone', profile.phone)
            profile.avatar = profile_data.get('avatar', profile.avatar)
            profile.save()

        return instance
