# Generated by Django 4.2.7 on 2023-12-02 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0009_alter_amazonproduct_rating_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amazonproduct',
            name='currency',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='نماد ارز'),
        ),
        migrations.DeleteModel(
            name='RainForestApiAccessHistory',
        ),
    ]
