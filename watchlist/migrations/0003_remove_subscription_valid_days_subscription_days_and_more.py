# Generated by Django 4.1.4 on 2022-12-24 14:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0002_alter_subscription_valid_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='valid_days',
        ),
        migrations.AddField(
            model_name='subscription',
            name='days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2023, 1, 23, 20, 15, 43, 683018)),
        ),
    ]
