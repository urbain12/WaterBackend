# Generated by Django 3.2 on 2021-11-09 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_alter_subscriptions_totalbalance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='TotalBalance',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]