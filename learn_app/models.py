# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Posts', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class Goals(models.Model):
    goal_id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Posts', models.DO_NOTHING)
    likes = models.IntegerField()
    publish_status = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goals'


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    likes = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    content = models.CharField(max_length=255)
    post_type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'posts'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    unikey = models.CharField(max_length=8, blank=True, null=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=50, blank=True, null=True)
    is_admin = models.IntegerField()
    account_status = models.IntegerField(blank=True, null=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
