# Generated by Django 2.1.2 on 2018-11-03 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20181103_2105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendancesheet',
            old_name='registered_students',
            new_name='registered',
        ),
    ]
