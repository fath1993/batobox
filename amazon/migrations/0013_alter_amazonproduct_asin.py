# Generated by Django 4.2.7 on 2023-12-08 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0012_alter_amazonproduct_asin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amazonproduct',
            name='asin',
            field=models.CharField(blank=True, max_length=255, unique=True, verbose_name='ASIN'),
        ),
    ]
