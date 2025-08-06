from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics", null=True, blank=True)

    def __str__(self):
        return self.username
