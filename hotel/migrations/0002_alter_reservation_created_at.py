# Generated by Django 5.0 on 2024-01-24 17:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
