# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_answer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-posted'], 'verbose_name': 'Answer', 'verbose_name_plural': 'Answers'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-posted'], 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AddField(
            model_name='answer',
            name='posted',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 2, 46, 28, 174425, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='posted',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 12, 2, 46, 39, 326714, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
