# Generated by Django 5.1.3 on 2024-12-20 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_alter_cartorder_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('delivered', 'Delivered'), ('Processing', 'Processing'), ('shipped', 'Shipped')], default='Processing', max_length=200),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='product_status',
            field=models.CharField(choices=[('delivered', 'Delivered'), ('Processing', 'Processing'), ('shipped', 'Shipped')], default='Processing', max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('draft', 'Draft'), ('published', 'Published'), ('rejected', 'Rejected'), ('in_review', 'In Review')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[('5', '⭐⭐⭐⭐⭐'), ('4', '⭐⭐⭐⭐☆'), ('3', '⭐⭐⭐☆☆'), ('2', '⭐⭐☆☆'), ('1', '⭐☆☆☆☆')], default=None),
        ),
    ]