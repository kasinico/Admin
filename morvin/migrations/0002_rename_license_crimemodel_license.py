# Generated by Django 3.2.14 on 2022-12-16 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('morvin', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crimemodel',
            old_name='License',
            new_name='license',
        ),
    ]
