# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommend', '0003_userpreference'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBookRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=5)),
                ('book', models.ForeignKey(to='recommend.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='userpreference',
            name='book',
        ),
        migrations.RemoveField(
            model_name='userpreference',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserPreference',
        ),
    ]
