# Generated by Django 3.2.7 on 2021-10-30 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_forum', '0008_auto_20211025_0352'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='is_active',
            field=models.IntegerField(default=1),
        ),
    ]
