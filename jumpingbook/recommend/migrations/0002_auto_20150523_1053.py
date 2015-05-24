# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='published_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
