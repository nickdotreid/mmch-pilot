# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=160, blank=True)),
                ('sent', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('active', models.BooleanField(default=True)),
                ('blacklist', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='numbers', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Number',
                'verbose_name_plural': 'Numbers',
            },
            bases=(models.Model,),
        ),
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
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(related_name='messages_to', blank=True, to='sms.Number', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='response_to',
            field=models.ForeignKey(related_name='responses', blank=True, to='sms.Message', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='messages_from', blank=True, to='sms.Number', null=True),
            preserve_default=True,
        ),
    ]
