# Generated by Django 3.2.9 on 2021-11-26 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_merge_20211116_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='HOTELLIST',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('owner', models.CharField(blank=True, max_length=200)),
                ('rating', models.CharField(blank=True, max_length=200)),
                ('district', models.CharField(blank=True, max_length=200)),
                ('Image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
