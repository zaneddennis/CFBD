# Generated by Django 2.2.2 on 2020-06-13 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_formation_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='offFormations',
            field=models.ManyToManyField(null=True, to='main.Formation'),
        ),
    ]