# Generated by Django 3.2.20 on 2023-12-22 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_auto_20231216_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='second_pdf',
        ),
        migrations.RemoveField(
            model_name='user',
            name='third_pdf',
        ),
    ]