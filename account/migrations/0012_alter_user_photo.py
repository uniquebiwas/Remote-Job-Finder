# Generated by Django 3.2.20 on 2023-11-25 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, default='images/default_image.png', null=True, upload_to='images'),
        ),
    ]