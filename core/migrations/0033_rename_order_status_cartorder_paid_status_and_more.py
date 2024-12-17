# Generated by Django 5.1.3 on 2024-12-13 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_product_sku_alter_product_product_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartorder',
            old_name='order_status',
            new_name='paid_status',
        ),
        migrations.AddField(
            model_name='cartorder',
            name='product_status',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('rejected', 'Rejected'), ('draft', 'Draft'), ('in_review', 'In Review'), ('disabled', 'Disabled'), ('published', 'Published')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[('4', '⭐⭐⭐⭐☆'), ('3', '⭐⭐⭐☆☆'), ('5', '⭐⭐⭐⭐⭐'), ('1', '⭐☆☆☆☆'), ('2', '⭐⭐☆☆')], default=None),
        ),
    ]
