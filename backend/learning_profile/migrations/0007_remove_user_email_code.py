# Generated by Django 3.2.7 on 2021-10-31 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_profile', '0006_alter_user_email_code_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_code',
        ),
    ]