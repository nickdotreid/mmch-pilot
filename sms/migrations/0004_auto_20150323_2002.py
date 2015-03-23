# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sms', '0003_auto_20150323_0108'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationPin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pin', models.CharField(max_length=10)),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('number', models.ForeignKey(to='sms.Number')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'RegistrationPin',
                'verbose_name_plural': 'RegistrationPins',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(max_length=160, blank=True),
            preserve_default=True,
        ),
    ]
