# Generated by Django 5.1.3 on 2024-12-23 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authens', '0004_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='county',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
    ]
