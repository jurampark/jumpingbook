# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcomments',
            name='book',
            field=models.ForeignKey(default=1, to='core.Book'),
            preserve_default=False,
        ),
    ]
