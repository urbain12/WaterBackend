# Generated by Django 3.2 on 2021-08-02 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_subscriptions_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='Extra',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]