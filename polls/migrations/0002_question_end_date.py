# Generated by Django 3.1 on 2020-09-16 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=None, null=True, verbose_name='date ended'),
        ),
    ]
