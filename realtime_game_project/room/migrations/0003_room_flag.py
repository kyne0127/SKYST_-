# Generated by Django 5.0.3 on 2024-03-23 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_room_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='flag',
            field=models.IntegerField(default=0),
        ),
    ]