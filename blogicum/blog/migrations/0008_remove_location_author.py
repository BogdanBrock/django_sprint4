# Generated by Django 3.2.16 on 2024-01-21 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20240121_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='author',
        ),
    ]