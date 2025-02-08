# Generated by Django 4.2.18 on 2025-02-08 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_remove_class_capacity_alter_booking_gym_class_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='class_status',
            field=models.IntegerField(choices=[(0, 'Confirmed'), (1, 'Cancelled'), (2, 'Completed')], default=0),
        ),
    ]
