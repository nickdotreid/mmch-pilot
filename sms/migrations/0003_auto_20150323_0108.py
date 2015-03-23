# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='number',
            name='user',
            field=models.ForeignKey(related_name='numbers', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
