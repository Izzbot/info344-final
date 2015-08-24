# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nice_simple_app', '0002_comparison_profile_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='nice_simple_app', default=1),
            preserve_default=False,
        ),
    ]
