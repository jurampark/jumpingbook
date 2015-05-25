import json
from braces.views import CsrfExemptMixin, LoginRequiredMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View
from recommend.models import Book, UserBookRating


class BookListView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        already_rating_book_list = request.user.userbookrating_set.values_list('book_id', flat=True)
        books = Book.objects.exclude(id__in=already_rating_book_list).values("id", "name", "author", "publisher", "published_date")

        return HttpResponse(json.dumps(list(books), cls=DjangoJSONEncoder), content_type="application/json")

class RatingBookView(CsrfExemptMixin, View):

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item-id')
        rating = request.POST.get('rating')

        try:
            user_book_rating = UserBookRating.objects.create(user=request.user,book=Book.objects.get(id=item_id),score=rating*2)
        except Exception as e:
            return HttpResponseBadRequest()

        return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json")
