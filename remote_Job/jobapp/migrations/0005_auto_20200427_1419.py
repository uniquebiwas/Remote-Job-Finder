# Generated by Django 3.0 on 2023-09-27 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0004_auto_20200427_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
