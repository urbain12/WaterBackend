# Generated by Django 3.2.9 on 2022-02-05 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery',
            field=models.BooleanField(default=False),
        ),
    ]