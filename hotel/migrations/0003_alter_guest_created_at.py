# Generated by Django 5.0 on 2024-01-24 17:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_alter_reservation_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]