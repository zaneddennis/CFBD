# Generated by Django 2.2.2 on 2020-05-07 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_playerteam'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='school',
        ),
    ]
