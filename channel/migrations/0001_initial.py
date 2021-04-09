# Generated by Django 2.2 on 2021-04-06 08:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('invite_link', models.UUIDField(default=uuid.uuid4)),
                ('consultant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='User.ConsultantProfile', verbose_name='channel owner')),
            ],
            options={
                'verbose_name_plural': 'Channel',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.Channel', verbose_name='')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.UserProfile', verbose_name='')),
            ],
            options={
                'verbose_name_plural': 'Subscription',
            },
        ),
        migrations.AddField(
            model_name='channel',
            name='subscribers',
            field=models.ManyToManyField(through='channel.Subscription', to='User.UserProfile', verbose_name=''),
        ),
    ]