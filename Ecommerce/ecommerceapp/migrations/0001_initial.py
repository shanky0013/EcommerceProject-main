# Generated by Django 4.2 on 2023-07-08 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('desc', models.TextField(max_length=500)),
                ('phone_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('itemList', models.CharField(max_length=5000)),
                ('name', models.CharField(max_length=100)),
                ('address1', models.CharField(max_length=1000)),
                ('address2', models.CharField(max_length=1000)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pin_code', models.CharField(max_length=100)),
                ('oid', models.CharField(max_length=100)),
                ('totalAmount', models.IntegerField(default=0)),
                ('paid', models.CharField(blank=True, max_length=500, null=True)),
                ('paymentstatus', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='OrderUpdate',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default='')),
                ('updated_desc', models.CharField(max_length=5000)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('delivered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prodname', models.CharField(max_length=100)),
                ('prodprice', models.IntegerField(default=0)),
                ('category', models.CharField(max_length=100)),
                ('subcategory', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=100)),
                ('prodimg', models.ImageField(upload_to='images')),
            ],
        ),
    ]
