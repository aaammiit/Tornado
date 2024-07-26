# Generated by Django 5.0.7 on 2024-07-25 05:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Krima_App', '0002_pm_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Push_to_pm_file',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now=True)),
                ('my_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Krima_App.my_upload_file')),
            ],
        ),
    ]
