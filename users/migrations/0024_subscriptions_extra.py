# Generated by Django 3.2 on 2021-08-02 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_alter_waterbuyhistory_meternumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='Extra',
            field=models.IntegerField(blank=True, default=0, max_length=255, null=True),
        ),
    ]
