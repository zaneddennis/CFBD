# Generated by Django 2.2.2 on 2020-06-10 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_game_plays'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('backs', models.IntegerField(default=0)),
                ('ends', models.IntegerField(default=0)),
                ('wideouts', models.IntegerField(default=0)),
            ],
        ),
    ]
