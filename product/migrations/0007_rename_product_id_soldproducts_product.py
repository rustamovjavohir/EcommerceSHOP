# Generated by Django 4.0.4 on 2022-05-17 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_rename_product_soldproducts_product_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='soldproducts',
            old_name='product_id',
            new_name='product',
        ),
    ]