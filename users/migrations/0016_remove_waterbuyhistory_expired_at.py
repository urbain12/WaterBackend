# Generated by Django 3.2 on 2021-07-18 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_tools_serialnumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waterbuyhistory',
            name='Expired_at',
        ),
    ]
