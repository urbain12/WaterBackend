# Generated by Django 3.2 on 2021-11-09 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_alter_subscriptions_tools'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='System2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system2', to='users.system'),
        ),
    ]
