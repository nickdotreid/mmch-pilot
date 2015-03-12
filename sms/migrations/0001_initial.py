# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_twilio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Number',
            fields=[
                ('caller_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='django_twilio.Caller')),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(related_name='numbers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Number',
                'verbose_name_plural': 'Numbers',
            },
            bases=('django_twilio.caller',),
        ),
    ]
