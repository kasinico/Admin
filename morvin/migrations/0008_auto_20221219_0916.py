# Generated by Django 3.2.14 on 2022-12-19 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morvin', '0007_auto_20221219_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='crimemodel',
            name='datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='crimemodel',
            table='morvin_crimemodel',
        ),
    ]
