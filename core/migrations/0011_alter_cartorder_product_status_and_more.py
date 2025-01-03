# Generated by Django 5.1.3 on 2024-12-01 17:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_product_category_alter_product_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('delivered', 'Delivered'), ('process', 'Processing'), ('shipped', 'Shipped')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='core.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('published', 'Published'), ('in_review', 'In Review'), ('draft', 'Draft'), ('disabled', 'Disabled'), ('rejected', 'Rejected')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(3, '⭐⭐⭐'), (1, '⭐'), (5, '⭐⭐⭐⭐⭐'), (2, '⭐⭐'), (4, '⭐⭐⭐⭐ ')], default=None),
        ),
    ]
