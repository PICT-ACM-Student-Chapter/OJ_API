# Generated by Django 3.1.14 on 2022-09-24 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_auto_20220924_2242'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='hacking_incorrect_code',
        ),
        migrations.RemoveField(
            model_name='question',
            name='hacking_incorrect_code_lang',
        ),
    ]