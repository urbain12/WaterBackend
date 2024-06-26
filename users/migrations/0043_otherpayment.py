# Generated by Django 3.2.10 on 2022-08-15 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0042_waterbuyhistory_transactionid'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Paidamount', models.CharField(blank=True, max_length=255, null=True)),
                ('PaymentDate', models.DateField(blank=True, null=True)),
                ('Description', models.TextField(blank=True)),
                ('CustomerID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
            ],
        ),
    ]
