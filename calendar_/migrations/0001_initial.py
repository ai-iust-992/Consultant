# Generated by Django 2.2 on 2021-04-06 08:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultantTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('cost', models.FloatField(default=0)),
                ('user_grade', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('user_comment', models.TextField(blank=True, max_length=500, null=True)),
                ('consultant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='User.ConsultantProfile')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='User.UserProfile')),
            ],
        ),
    ]
