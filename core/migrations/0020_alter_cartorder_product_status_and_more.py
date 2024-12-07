# Generated by Django 5.1.3 on 2024-12-03 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_cartorder_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('shipped', 'Shipped'), ('process', 'Processing'), ('delivered', 'Delivered')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('published', 'Published'), ('draft', 'Draft'), ('rejected', 'Rejected'), ('in_review', 'In Review')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviews', to='core.product'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(4, '⭐⭐⭐⭐ '), (5, '⭐⭐⭐⭐⭐'), (3, '⭐⭐⭐'), (1, '⭐'), (2, '⭐⭐')], default=None),
        ),
    ]
