# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0010_externalprotocol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalprotocol',
            name='shortname',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='externalprotocol',
            name='url',
            field=models.URLField(),
        ),
    ]
