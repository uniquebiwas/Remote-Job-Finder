# Generated by Django 3.2.20 on 2024-01-15 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]