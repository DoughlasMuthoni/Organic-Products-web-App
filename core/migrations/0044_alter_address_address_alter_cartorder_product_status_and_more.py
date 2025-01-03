# Generated by Django 5.1.3 on 2024-12-23 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_remove_cartitem_purchase_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('delivered', 'Delivered'), ('shipped', 'Shipped')], default='Processing', max_length=200),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='product_status',
            field=models.CharField(choices=[('Processing', 'Processing'), ('delivered', 'Delivered'), ('shipped', 'Shipped')], default='Processing', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('published', 'Published'), ('rejected', 'Rejected'), ('draft', 'Draft'), ('in_review', 'In Review'), ('disabled', 'Disabled')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[('2', '⭐⭐☆☆'), ('1', '⭐☆☆☆☆'), ('4', '⭐⭐⭐⭐☆'), ('5', '⭐⭐⭐⭐⭐'), ('3', '⭐⭐⭐☆☆')], default=None),
        ),
    ]
