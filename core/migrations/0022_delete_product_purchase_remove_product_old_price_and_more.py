# Generated by Django 5.1.3 on 2024-12-06 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_product_purchase_remove_product_specifications_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product_purchase',
        ),
        migrations.RemoveField(
            model_name='product',
            name='old_price',
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('shipped', 'Shipped'), ('process', 'Processing'), ('delivered', 'Delivered')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('published', 'Published'), ('in_review', 'In Review'), ('disabled', 'Disabled'), ('draft', 'Draft'), ('rejected', 'Rejected')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(1, '⭐'), (2, '⭐⭐'), (3, '⭐⭐⭐'), (5, '⭐⭐⭐⭐⭐'), (4, '⭐⭐⭐⭐ ')], default=None),
        ),
    ]
