# Generated by Django 3.1.4 on 2020-12-25 06:47

import contest.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20201222_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='banner_image',
            field=models.FileField(null=True, upload_to=contest.models.upload_contest_banner),
        ),
    ]
