# Generated by Django 3.2 on 2021-05-11 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_subscriptions_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
