# Generated by Django 2.1.1 on 2018-11-26 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20181126_0051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registeredgroup',
            old_name='delete_by',
            new_name='deleted_by',
        ),
    ]
