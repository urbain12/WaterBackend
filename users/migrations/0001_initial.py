# Generated by Django 3.2 on 2021-08-08 19:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='background',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=200)),
                ('Details', models.TextField(blank=True)),
                ('Image', models.ImageField(blank=True, null=True, upload_to='')),
                ('Published_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(blank=True, max_length=255, null=True)),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(blank=True, max_length=255, null=True)),
                ('LastName', models.CharField(blank=True, max_length=255, null=True)),
                ('IDnumber', models.CharField(blank=True, max_length=255, null=True)),
                ('Province', models.CharField(blank=True, max_length=255, null=True)),
                ('District', models.CharField(blank=True, max_length=255, null=True)),
                ('Sector', models.CharField(blank=True, max_length=255, null=True)),
                ('Cell', models.CharField(blank=True, max_length=255, null=True)),
                ('Language', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerMeter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_phone', models.CharField(blank=True, max_length=255, null=True)),
                ('meter', models.CharField(blank=True, max_length=255, null=True)),
                ('last_update', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Language', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('Meternumber', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Message', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('Disable', models.BooleanField(default=False)),
                ('inStock', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Names', models.CharField(blank=True, max_length=255, null=True)),
                ('Message', models.TextField(blank=True)),
                ('phonenumber', models.CharField(blank=True, max_length=255, null=True)),
                ('reply', models.TextField(blank=True, default='Please wait for the response', null=True)),
                ('Province', models.CharField(blank=True, max_length=255, null=True)),
                ('District', models.CharField(blank=True, max_length=255, null=True)),
                ('Sector', models.CharField(blank=True, max_length=255, null=True)),
                ('Cell', models.CharField(blank=True, max_length=255, null=True)),
                ('Language', models.CharField(blank=True, max_length=255, null=True)),
                ('service', models.CharField(blank=True, max_length=255, null=True)),
                ('replied', models.BooleanField(default=False)),
                ('send_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(blank=True, max_length=255, null=True)),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('From', models.DateTimeField(blank=True, null=True)),
                ('To', models.DateTimeField(blank=True, null=True)),
                ('TotalBalance', models.CharField(blank=True, max_length=255, null=True)),
                ('Extra', models.IntegerField(blank=True, default=0, null=True)),
                ('complete', models.BooleanField(default=False)),
                ('Category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.category')),
                ('CustomerID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ToolsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WaterBuyHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Amount', models.CharField(blank=True, max_length=255, null=True)),
                ('Token', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Meternumber', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.meters')),
            ],
        ),
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
                ('Amount', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('CategoryID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.toolscategory')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionsTools',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('SubscriptionsID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.subscriptions')),
                ('ToolID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.tools')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionsPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Paidamount', models.CharField(blank=True, max_length=255, null=True)),
                ('Paid', models.BooleanField(default=False)),
                ('PaidMonth', models.DateField(blank=True, null=True)),
                ('PaymentDate', models.DateField(blank=True, null=True)),
                ('SubscriptionsID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.subscriptions')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('names', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.product')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='Meternumber',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.meters'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
