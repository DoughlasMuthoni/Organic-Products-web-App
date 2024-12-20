# Generated by Django 5.1.3 on 2024-12-11 08:11

import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_remove_product_sku_alter_product_product_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890 ', length=4, max_length=10, prefix='sku', unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('disabled', 'Disabled'), ('draft', 'Draft'), ('published', 'Published'), ('rejected', 'Rejected'), ('in_review', 'In Review')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[('3', '⭐⭐⭐☆☆'), ('1', '⭐☆☆☆☆'), ('5', '⭐⭐⭐⭐⭐'), ('4', '⭐⭐⭐⭐☆'), ('2', '⭐⭐☆☆')], default=None),
        ),
    ]
