# Generated by Django 3.1.4 on 2020-12-22 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contest', '0001_initial'),
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestque',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.question'),
        ),
        migrations.AddField(
            model_name='contest',
            name='questions',
            field=models.ManyToManyField(related_name='contests', through='contest.ContestQue', to='question.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='contestque',
            unique_together={('contest', 'order')},
        ),
    ]