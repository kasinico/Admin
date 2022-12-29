# Generated by Django 3.2.14 on 2022-12-27 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morvin', '0013_chatmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrimeCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
            ],
        ),
        migrations.AlterModelTable(
            name='crimemodel',
            table='crimemodel',
        ),
    ]