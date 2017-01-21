# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0025_auto_20170105_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='basicdataset',
            name='experimentIdea',
            field=models.TextField(max_length=130, blank=True),
        ),
        migrations.AlterField(
            model_name='basicdataset',
            name='hypothesis',
            field=models.TextField(max_length=600, blank=True),
        ),
        migrations.AlterField(
            model_name='basicdataset',
            name='researchObjective',
            field=models.TextField(max_length=1200, blank=True),
        ),
        migrations.AlterField(
            model_name='basicdataset',
            name='shortTitle',
            field=models.CharField(max_length=60),
        ),
        migrations.AddField(
            model_name='publication',
            name='dataset',
            field=models.ForeignKey(to='protocoltool.BasicDataset'),
        ),
    ]
