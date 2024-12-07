# Generated by Django 5.1.3 on 2024-12-01 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_cartorder_product_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendors',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(choices=[('shipped', 'Shipped'), ('process', 'Processing'), ('delivered', 'Delivered')], default='processing', max_length=30),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('published', 'Published'), ('rejected', 'Rejected'), ('in_review', 'In Review')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendors', to='core.vendors'),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(4, '⭐⭐⭐⭐ '), (5, '⭐⭐⭐⭐⭐'), (2, '⭐⭐'), (1, '⭐'), (3, '⭐⭐⭐')], default=None),
        ),
    ]
