# Generated by Django 5.1.4 on 2025-07-11 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jewelleryapp', '0019_subcategories_product_subcategories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subcategories',
            old_name='name',
            new_name='sub_name',
        ),
    ]
