# Generated by Django 3.1.4 on 2020-12-22 07:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import question.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('score', models.IntegerField()),
                ('input_format', models.TextField(default='')),
                ('output_format', models.TextField(default='')),
                ('constraints', models.TextField(default='')),
                ('correct_code', models.TextField(blank=True, null=True)),
                ('correct_code_lang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.language')),
            ],
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('input', models.FileField(upload_to=question.models.upload_input_rename)),
                ('output', models.FileField(upload_to=question.models.upload_output_rename)),
                ('is_public', models.BooleanField(default=False)),
                ('weightage', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('que_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_cases', to='question.question')),
            ],
        ),
    ]
