# Generated by Django 2.2.2 on 2020-06-14 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_defensiveformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='defFormations',
            field=models.ManyToManyField(to='main.DefensiveFormation'),
        ),
    ]