# Generated by Django 3.2.7 on 2021-10-25 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_profile', '0004_auto_20211025_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_code_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]