# Generated by Django 5.1.3 on 2024-12-01 21:59

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_vendors_date_alter_cartorder_product_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendors',
            name='cover_image',
            field=models.ImageField(default='category.png', upload_to=core.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('process', 'Processing'), ('delivered', 'Delivered'), ('shipped', 'Shipped')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('in_review', 'In Review'), ('disabled', 'Disabled'), ('published', 'Published'), ('draft', 'Draft'), ('rejected', 'Rejected')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(2, '⭐⭐'), (5, '⭐⭐⭐⭐⭐'), (4, '⭐⭐⭐⭐ '), (1, '⭐'), (3, '⭐⭐⭐')], default=None),
        ),
    ]
