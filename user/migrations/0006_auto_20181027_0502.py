# Generated by Django 2.0.1 on 2018-10-27 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_attendancesheet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='student',
        ),
        migrations.AlterField(
            model_name='group',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to=settings.AUTH_USER_MODEL),
        ),
    ]
