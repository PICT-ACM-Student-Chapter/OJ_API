# Generated by Django 3.1.3 on 2020-11-10 22:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('question', '0003_auto_20201110_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('input', models.FileField(upload_to='')),
            ],
        ),
    ]
