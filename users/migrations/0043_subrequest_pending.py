# Generated by Django 3.2.10 on 2022-08-14 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0042_waterbuyhistory_transactionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='subrequest',
            name='Pending',
            field=models.BooleanField(default=False),
        ),
    ]
