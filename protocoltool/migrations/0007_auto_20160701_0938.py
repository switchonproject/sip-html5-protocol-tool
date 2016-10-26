# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0006_partner_organisation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datareq',
            old_name='description',
            new_name='task',
        ),
        migrations.RenameField(
            model_name='expstep',
            old_name='description',
            new_name='task',
        ),
        migrations.RenameField(
            model_name='reporting',
            old_name='description',
            new_name='task',
        ),
    ]
