from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """redefine a new default user model"""
    unikey = models.CharField(max_length=8, blank=True, null=True)
    account_status = models.IntegerField(blank=True, null=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username