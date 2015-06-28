from django.contrib.auth.models import User
from django.db import models

from core.models import TimeStampedModel

class UserBookRating(TimeStampedModel):
    user = models.ForeignKey(User)
    book = models.ForeignKey('core.Book')
    score = models.IntegerField(default=5, null=False) # 1~10

    class Meta:
        unique_together=(("user","book"),)


class UserBookBlackList(TimeStampedModel):
    user = models.ForeignKey(User)
    book = models.ForeignKey('core.Book')

    class Meta:
        unique_together=(("user","book"),)

class UserBookWishList(TimeStampedModel):
    user = models.ForeignKey(User)
    book = models.ForeignKey('core.Book')

    class Meta:
        unique_together=(("user","book"),)