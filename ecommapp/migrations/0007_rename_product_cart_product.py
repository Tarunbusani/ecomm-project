# Generated by Django 4.2.4 on 2023-09-06 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0006_alter_cart_product_alter_cart_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product',
            new_name='Product',
        ),
    ]
