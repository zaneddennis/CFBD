# Generated by Django 2.2.2 on 2020-07-19 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0050_coach_defformations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coach',
            name='defFormations',
        ),
        migrations.AddField(
            model_name='coach',
            name='defBase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.DefensiveFormation'),
        ),
    ]