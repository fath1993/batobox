# Generated by Django 4.2.7 on 2023-11-30 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('amazon', '0002_rainforestapiaccesshistory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rainforestapiaccesshistory',
            name='created_by',
            field=models.ForeignKey(default=1, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ایجاد شده توسط'),
            preserve_default=False,
        ),
    ]
