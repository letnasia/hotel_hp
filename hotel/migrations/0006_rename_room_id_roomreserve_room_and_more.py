# Generated by Django 5.0 on 2024-01-03 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_rename_id_guest_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomreserve',
            old_name='room_id',
            new_name='room',
        ),
        migrations.AlterUniqueTogether(
            name='roomreserve',
            unique_together={('date', 'room')},
        ),
    ]
