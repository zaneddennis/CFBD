# Generated by Django 2.2.2 on 2020-05-04 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20200502_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='jersey',
            field=models.IntegerField(default=1),
        ),
    ]
