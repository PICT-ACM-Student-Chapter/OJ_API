# Generated by Django 3.1.14 on 2022-09-21 18:41

import contest.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20210303_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='banner_image',
            field=models.FileField(blank=True, default='nopath', upload_to=contest.models.upload_contest_banner),
            preserve_default=False,
        ),
    ]
