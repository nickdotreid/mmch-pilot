# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=160)),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('reciever', models.ForeignKey(related_name='messages_to', blank=True, to='sms.Number', null=True)),
                ('sender', models.ForeignKey(related_name='messages_from', blank=True, to='sms.Number', null=True)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
    ]
