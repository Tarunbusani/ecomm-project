# Generated by Django 4.2.4 on 2023-09-07 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0009_rename_customer_orderplaced_customers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderplaced',
            old_name='Customers',
            new_name='Customer',
        ),
        migrations.RenameField(
            model_name='orderplaced',
            old_name='Products',
            new_name='Product',
        ),
    ]