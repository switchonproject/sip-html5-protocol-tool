# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasicDataset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('experimentIdea', models.TextField(blank=True)),
                ('hypothesis', models.TextField(blank=True)),
                ('researchObjective', models.TextField(blank=True)),
                ('principles', models.TextField(blank=True)),
                ('dateLastUpdate', models.DateField(default=datetime.date.today, blank=True)),
                ('published', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DataReq',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('properties', models.TextField(blank=True)),
                ('deadline', models.DateField(default=datetime.date.today, blank=True)),
                ('dataset', models.ForeignKey(to='protocoltool.BasicDataset')),
            ],
        ),
        migrations.CreateModel(
            name='ExpStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('output', models.TextField(blank=True)),
                ('deadline', models.DateField(default=datetime.date.today, blank=True)),
                ('dataset', models.ForeignKey(to='protocoltool.BasicDataset')),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('lead', models.BooleanField(default=False)),
                ('dataset', models.ForeignKey(to='protocoltool.BasicDataset')),
            ],
        ),
        migrations.CreateModel(
            name='ResultRep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(blank=True)),
                ('output', models.TextField(blank=True)),
                ('deadline', models.DateField(default=datetime.date.today, blank=True)),
                ('dataset', models.ForeignKey(to='protocoltool.BasicDataset')),
                ('partner', models.ForeignKey(to='protocoltool.Partner')),
            ],
        ),
        migrations.AddField(
            model_name='expstep',
            name='partner',
            field=models.ForeignKey(to='protocoltool.Partner'),
        ),
        migrations.AddField(
            model_name='datareq',
            name='partner',
            field=models.ForeignKey(to='protocoltool.Partner'),
        ),
    ]
