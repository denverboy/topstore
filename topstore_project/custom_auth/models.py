from django.contrib.auth.models import User
from django.db import models


def profile_avatar_directory_path(instance, filename):
    return f'profiles/profile#{instance.pk}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=profile_avatar_directory_path,
    )

    def __str__(self):
        return f'Profile of {self.user.username}'
