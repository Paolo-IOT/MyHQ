# Generated by Django 5.0.3 on 2024-04-18 04:59

import hqmanager.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hqmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='immagine',
            field=models.ImageField(blank=True, null=True, upload_to=hqmanager.models.event_directory_path),
        ),
    ]