# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0027_auto_20170123_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='publication',
            name='type',
            field=models.CharField(max_length=250),
        ),
    ]
