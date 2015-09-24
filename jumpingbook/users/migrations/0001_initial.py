# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBookBlackList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(to='core.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBookRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('score', models.IntegerField(default=5)),
                ('book', models.ForeignKey(to='core.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBookWishList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('book', models.ForeignKey(to='core.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFriend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('friend', models.ForeignKey(related_name='assignee', to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userfriend',
            unique_together=set([('user', 'friend')]),
        ),
        migrations.AlterUniqueTogether(
            name='userbookwishlist',
            unique_together=set([('user', 'book')]),
        ),
        migrations.AlterUniqueTogether(
            name='userbookrating',
            unique_together=set([('user', 'book')]),
        ),
        migrations.AlterUniqueTogether(
            name='userbookblacklist',
            unique_together=set([('user', 'book')]),
        ),
    ]
