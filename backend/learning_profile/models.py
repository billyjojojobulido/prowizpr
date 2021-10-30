from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(models.Manager):
    # retrieve all the users admins could manage
    def admin_manage_users(self):
        users = self.filter(is_superuser=False)
        return users


# Create your models here.
class User(AbstractUser):
    """redefine a new default user model"""
    account_status = models.IntegerField(blank=True, null=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    email_code = models.CharField(max_length=10, blank=True, null=True)
    email_code_time = models.IntegerField(blank=True, null=False, default=0)
    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'User'

    def __str__(self):
        return self.username
