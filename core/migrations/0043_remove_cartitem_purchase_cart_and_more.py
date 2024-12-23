# Generated by Django 5.1.3 on 2024-12-23 12:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_alter_cartorder_order_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem_purchase',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem_purchase',
            name='product',
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='price',
            field=models.DecimalField(decimal_places=2, default='1.99', max_digits=12),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('delivered', 'Delivered'), ('shipped', 'Shipped'), ('Processing', 'Processing')], default='Processing', max_length=200),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='price',
            field=models.DecimalField(decimal_places=2, default=100.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='product_status',
            field=models.CharField(choices=[('delivered', 'Delivered'), ('shipped', 'Shipped'), ('Processing', 'Processing')], default='Processing', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.DecimalField(decimal_places=2, default='2.99', max_digits=12),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default='1.99', max_digits=12),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('rejected', 'Rejected'), ('published', 'Published'), ('disabled', 'Disabled'), ('in_review', 'In Review')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[('2', '⭐⭐☆☆'), ('1', '⭐☆☆☆☆'), ('3', '⭐⭐⭐☆☆'), ('5', '⭐⭐⭐⭐⭐'), ('4', '⭐⭐⭐⭐☆')], default=None),
        ),
        migrations.DeleteModel(
            name='Cart_purchase',
        ),
        migrations.DeleteModel(
            name='CartItem_purchase',
        ),
    ]
