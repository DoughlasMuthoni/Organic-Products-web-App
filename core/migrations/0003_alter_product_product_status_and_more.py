# Generated by Django 5.1.3 on 2024-11-30 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_product_tags_alter_cartorder_product_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('in_review', 'In Review'), ('rejected', 'Rejected'), ('disabled', 'Disabled')], default='in_review', max_length=100),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(1, '⭐'), (5, '⭐⭐⭐⭐⭐'), (3, '⭐⭐⭐'), (2, '⭐⭐'), (4, '⭐⭐⭐⭐ ')], default=None),
        ),
    ]
