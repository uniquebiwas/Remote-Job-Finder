# Generated by Django 3.2.20 on 2023-10-01 13:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_user_pdf_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pdf_document',
            field=models.FileField(default=django.utils.timezone.now, upload_to='pdf_documents/'),
            preserve_default=False,
        ),
    ]