# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0028_auto_20170201_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expstep',
            name='links',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='reporting',
            name='links',
            field=models.TextField(blank=True),
        ),
    ]
