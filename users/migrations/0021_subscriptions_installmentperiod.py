# Generated by Django 3.2 on 2021-11-03 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20211028_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='InstallmentPeriod',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]