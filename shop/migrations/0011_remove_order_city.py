# Generated by Django 3.2.7 on 2021-10-16 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_customer_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
    ]
