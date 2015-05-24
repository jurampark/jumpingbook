import datetime
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return '%s' % self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('recommend.Category')
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    published_date = models.DateField(default=datetime.date.today)

# class UserPreference(models.Model):
#     User
#     Book
#     score