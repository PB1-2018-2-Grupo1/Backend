# Generated by Django 2.1.1 on 2018-11-26 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_merge_20181122_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredgroup',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]