# Generated by Django 2.2.2 on 2020-06-06 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_auto_20200510_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='drives',
            field=models.CharField(blank=True, max_length=999999, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(choices=[('QB', 'Quarterback'), ('RB', 'Running Back'), ('WR', 'Wide Receiver'), ('TE', 'Tight End'), ('OL', 'Offensive Line'), ('DT', 'Defensive Tackle'), ('EDGE', 'Edge Defender'), ('LB', 'Linebacker'), ('CB', 'Cornerback'), ('S', 'Safety'), ('K', 'Kicker'), ('P', 'Punter')], max_length=4),
        ),
    ]
