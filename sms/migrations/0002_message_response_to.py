# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='response_to',
            field=models.ForeignKey(related_name='responses', blank=True, to='sms.Message', null=True),
            preserve_default=True,
        ),
    ]
