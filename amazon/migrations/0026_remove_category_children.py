# Generated by Django 4.2.7 on 2024-01-05 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0025_alter_addamazonproduct_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='children',
        ),
    ]
