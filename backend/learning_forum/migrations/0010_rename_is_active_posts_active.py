# Generated by Django 3.2.7 on 2021-10-30 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_forum', '0009_posts_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='is_active',
            new_name='active',
        ),
    ]
