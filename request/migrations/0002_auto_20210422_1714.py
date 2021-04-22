# Generated by Django 2.2 on 2021-04-22 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='joinchannelrequest',
            name='request_type',
            field=models.CharField(choices=[('secretary', 'secretary'), ('join_channel', 'join_channel')], default='join_channel', max_length=64),
        ),
        migrations.AddField(
            model_name='secretaryrequest',
            name='request_type',
            field=models.CharField(choices=[('secretary', 'secretary'), ('join_channel', 'join_channel')], default='join_channel', max_length=64),
        ),
    ]
