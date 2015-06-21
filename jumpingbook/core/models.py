import datetime
from django.db import models

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return '%s' % self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    category = models.ForeignKey('core.Category')
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    published_date = models.DateField(default=datetime.date.today)

    # @property
    # def total_score(self):
    #     sum = self.userbookrating_set.aggregate(Sum('score'))
    #     return sum