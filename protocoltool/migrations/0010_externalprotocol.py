# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0009_basicdataset_shortname'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalProtocol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shortname', models.CharField(max_length=100)),
                ('url', models.URLField(max_length=100)),
                ('dateLastUpdate', models.DateField(default=datetime.date.today, blank=True)),
            ],
        ),
    ]
