# Generated by Django 3.2 on 2021-06-10 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='replied',
            field=models.BooleanField(default=False),
        ),
    ]
