# Generated by Django 2.2.2 on 2020-05-01 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_auto_20200430_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.School'),
        ),
    ]
