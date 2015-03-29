# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='published',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
