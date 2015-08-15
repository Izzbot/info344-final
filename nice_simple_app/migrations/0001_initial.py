# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comparison',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('collected_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('collected_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('collected_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('public_view', models.BooleanField(default=True)),
                ('img_url', models.URLField()),
                ('p_name', models.TextField(default='')),
                ('p_phone', models.CharField(default='', max_length=10)),
                ('p_city', models.CharField(default='', max_length=50)),
                ('p_region', models.CharField(default='', max_length=50)),
                ('p_country', models.CharField(default='', max_length=50)),
                ('p_birthday', models.CharField(default='', max_length=50)),
                ('p_birthyear', models.CharField(default='', max_length=4)),
                ('p_relationship', models.CharField(default='', max_length=50)),
                ('p_relationship_with', models.CharField(default='', max_length=50)),
                ('p_job_title', models.CharField(default='', max_length=50)),
                ('p_job_employer', models.CharField(default='', max_length=50)),
                ('p_studying', models.CharField(default='', max_length=50)),
                ('p_school', models.CharField(default='', max_length=50)),
                ('p_friends', models.IntegerField(default=0)),
                ('p_likes', models.IntegerField(default=0)),
                ('p_groups', models.IntegerField(default=0)),
                ('p_information', models.TextField(default='')),
                ('p_quotes', models.TextField(default='')),
                ('p_nickname', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='comparison',
            name='l_profile',
            field=models.ForeignKey(to='nice_simple_app.Profile', null=True, related_name='l_profile'),
        ),
        migrations.AddField(
            model_name='comparison',
            name='r_profile',
            field=models.ForeignKey(to='nice_simple_app.Profile', null=True, related_name='r_profile'),
        ),
    ]
