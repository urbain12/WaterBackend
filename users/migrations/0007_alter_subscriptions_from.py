# Generated by Django 3.2 on 2021-06-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_notification_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='From',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]