# Generated by Django 3.1.5 on 2021-03-02 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_contest_banner_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='ems_slot_id',
            field=models.CharField(default='sdfsdf', max_length=30),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name='contest',
            index=models.Index(fields=['ems_slot_id'], name='contest_con_ems_slo_a1a0b1_idx'),
        ),
    ]
