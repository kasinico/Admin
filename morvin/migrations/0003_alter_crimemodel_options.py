# Generated by Django 3.2.14 on 2022-12-17 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('morvin', '0002_rename_license_crimemodel_license'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crimemodel',
            options={'ordering': ['datetime']},
        ),
    ]