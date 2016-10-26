# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0019_auto_20161018_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicdataset',
            name='editUsers',
            field=models.ManyToManyField(related_name='edit_users', null=True, to='protocoltool.UserProfile'),
        ),
        migrations.AddField(
            model_name='basicdataset',
            name='leadUser',
            field=models.ForeignKey(related_name='lead_user', to='protocoltool.UserProfile', null=True),
        ),
    ]
