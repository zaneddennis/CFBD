# Generated by Django 2.2.2 on 2020-06-10 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_formation'),
    ]

    operations = [
        migrations.AddField(
            model_name='formation',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
