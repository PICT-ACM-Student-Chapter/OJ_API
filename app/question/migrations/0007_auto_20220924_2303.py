# Generated by Django 3.1.14 on 2022-09-24 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201230_1303'),
        ('question', '0006_auto_20220924_2302'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HackingCodes',
            new_name='HackingCode',
        ),
    ]
