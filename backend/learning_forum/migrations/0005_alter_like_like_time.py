# Generated by Django 3.2.7 on 2021-10-17 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_forum', '0004_posts_report_times'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='like_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
