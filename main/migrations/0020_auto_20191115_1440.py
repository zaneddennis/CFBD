# Generated by Django 2.2.2 on 2019-11-15 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='division',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='game',
            name='away',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='main.Team'),
        ),
        migrations.AlterField(
            model_name='game',
            name='home',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='main.Team'),
        ),
    ]