# Generated by Django 4.2.7 on 2023-11-30 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_transportcost_weight_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transportcost',
            name='currency',
        ),
        migrations.DeleteModel(
            name='Currency',
        ),
        migrations.DeleteModel(
            name='TransportCost',
        ),
    ]
