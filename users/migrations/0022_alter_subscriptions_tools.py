# Generated by Django 3.2 on 2021-11-07 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_subscriptions_installmentperiod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='Tools',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
