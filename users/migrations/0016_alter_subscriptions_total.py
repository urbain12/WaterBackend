# Generated by Django 3.2 on 2021-10-24 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_subscriptions_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='Total',
            field=models.IntegerField(blank=True, max_length=200, null=True),
        ),
    ]