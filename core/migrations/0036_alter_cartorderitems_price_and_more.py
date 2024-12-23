# Generated by Django 5.1.3 on 2024-12-18 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_alter_address_options_alter_cartorder_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorderitems',
            name='price',
            field=models.DecimalField(decimal_places=2, default='100', max_digits=999999999999),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='product_status',
            field=models.CharField(choices=[('delivered', 'Delivered'), ('shipped', 'Shipped'), ('process', 'Processing')], default='Processing', max_length=200),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='total',
            field=models.DecimalField(decimal_places=2, default='100', max_digits=999999999999),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('published', 'Published'), ('draft', 'Draft'), ('in_review', 'In Review'), ('disabled', 'Disabled'), ('rejected', 'Rejected')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(blank=True, default='organic', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[('3', '⭐⭐⭐☆☆'), ('5', '⭐⭐⭐⭐⭐'), ('2', '⭐⭐☆☆'), ('4', '⭐⭐⭐⭐☆'), ('1', '⭐☆☆☆☆')], default=None),
        ),
    ]
