# Generated by Django 3.2 on 2021-11-12 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_subscriptions_system2'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='subscriptions',
            name='discount1',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
