# Generated by Django 3.0 on 2023-09-27 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0003_auto_20200426_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='salary',
            field=models.IntegerField(blank=True),
        ),
    ]
