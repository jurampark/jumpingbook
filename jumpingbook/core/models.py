import datetime
from django.contrib.auth.models import User
from django.db import models

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    link_class = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return '%s' % self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    link_class = models.CharField(max_length=10) # for kyobo books scrapping
    category = models.ForeignKey('core.Category')

    def __unicode__(self):
        return '%s' % self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    barcode = models.CharField(max_length=20) # for kyobo books
    image_url = models.URLField()
    category = models.ForeignKey('core.SubCategory')
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    published_date = models.DateField(default=datetime.date.today)

    class Meta:
        unique_together=(("title","author"),)

    # @property
    # def total_score(self):
    #     sum = self.userbookrating_set.aggregate(Sum('score'))
    #     return sum

class BookComments(TimeStampedModel):
    user = models.ForeignKey(User, null=False)
    comment = models.TextField(null=False, blank=True)
