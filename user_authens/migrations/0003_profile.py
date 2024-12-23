# Generated by Django 5.1.3 on 2024-12-20 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_authens', '0002_user_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='image')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True)),
                ('bio', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
    ]
