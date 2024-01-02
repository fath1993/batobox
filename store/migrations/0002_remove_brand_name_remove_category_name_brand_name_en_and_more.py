# Generated by Django 4.2.7 on 2023-11-23 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='name',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.AddField(
            model_name='brand',
            name='name_en',
            field=models.CharField(default=1, max_length=255, verbose_name='نام انگلیسی'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brand',
            name='name_fa',
            field=models.CharField(default=1, max_length=255, verbose_name='نام فارسی'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(default=1, max_length=255, verbose_name='نام انگلیسی'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='name_fa',
            field=models.CharField(default=1, max_length=255, verbose_name='نام فارسی'),
            preserve_default=False,
        ),
    ]
