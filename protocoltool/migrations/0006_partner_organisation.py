# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0005_auto_20160624_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='organisation',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
