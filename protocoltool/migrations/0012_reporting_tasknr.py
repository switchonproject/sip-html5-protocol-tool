# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0011_auto_20160720_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporting',
            name='taskNr',
            field=models.IntegerField(default=1),
        ),
    ]
