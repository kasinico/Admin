# Generated by Django 3.2.14 on 2022-12-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morvin', '0009_remove_crimemodel_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='crimemodel',
            name='datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='crimemodel',
            name='stage',
            field=models.TextField(blank=True, null=True),
        ),
    ]
