# Generated by Django 3.2 on 2021-10-28 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20211027_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='From',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='To',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
