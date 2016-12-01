# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0020_auto_20161020_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicdataset',
            name='editUsers',
            field=models.ManyToManyField(related_name='edit_users', to='protocoltool.UserProfile'),
            preserve_default=True,
        ),
    ]
