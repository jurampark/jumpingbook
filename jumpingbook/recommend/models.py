import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from core.models import TimeStampedModel


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return '%s' % self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    category = models.ForeignKey('recommend.Category')
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    published_date = models.DateField(default=datetime.date.today)

    # @property
    # def total_score(self):
    #     sum = self.userbookrating_set.aggregate(Sum('score'))
    #     return sum

class UserBookRating(TimeStampedModel):
    user = models.ForeignKey(User)
    book = models.ForeignKey('recommend.Book')
    score = models.IntegerField(default=5, null=False)