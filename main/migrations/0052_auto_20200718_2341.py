# Generated by Django 2.2.2 on 2020-07-19 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_auto_20200718_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='defBase',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='main.DefensiveFormation'),
        ),
    ]
