# Generated by Django 3.2.7 on 2021-10-15 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_goal', '0002_tasks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goals',
            options={'verbose_name_plural': 'Goal'},
        ),
        migrations.AlterModelOptions(
            name='tasks',
            options={'verbose_name_plural': 'Task'},
        ),
    ]
