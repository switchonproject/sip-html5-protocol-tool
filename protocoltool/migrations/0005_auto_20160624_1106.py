# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0004_auto_20160624_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('properties', models.TextField(blank=True)),
                ('deadline', models.DateField(default=datetime.date.today, blank=True)),
                ('dataset', models.ForeignKey(to='protocoltool.BasicDataset')),
                ('partner', models.ForeignKey(to='protocoltool.Partner')),
            ],
        ),
        migrations.RemoveField(
            model_name='resultrep',
            name='dataset',
        ),
        migrations.RemoveField(
            model_name='resultrep',
            name='partner',
        ),
        migrations.DeleteModel(
            name='ResultRep',
        ),
    ]
