# Generated by Django 5.0 on 2024-01-05 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0011_menuitem_restaurants'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='role_id',
            new_name='role',
        ),
    ]