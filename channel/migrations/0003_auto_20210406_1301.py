# Generated by Django 2.2 on 2021-04-06 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0002_auto_20210406_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='invite_link',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
