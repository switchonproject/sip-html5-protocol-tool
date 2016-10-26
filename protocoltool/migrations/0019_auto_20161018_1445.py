# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0018_auto_20161006_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='organisation',
            field=models.CharField(default='organisation', max_length=100),
            preserve_default=False,
        ),
    ]
