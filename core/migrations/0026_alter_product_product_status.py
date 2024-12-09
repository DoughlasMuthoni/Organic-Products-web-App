# Generated by Django 5.1.3 on 2024-12-09 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_address_options_alter_product_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('published', 'Published'), ('rejected', 'Rejected'), ('in_review', 'In Review'), ('draft', 'Draft'), ('disabled', 'Disabled')], default='in_review', max_length=100),
        ),
    ]
