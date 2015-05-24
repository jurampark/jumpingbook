import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from recommend.models import Book


class BookListView(View):
    def post(self, request, *args, **kwargs):
        books = Book.objects.values("id", "name", "author", "publisher", "published_date")

        books_json = json.dumps(list(books), cls=DjangoJSONEncoder)

        # data = simplejson.dumps(books)
        # data = serializers.serialize("xml", SomeModel.objects.all())

        # return HttpResponse(data, mimetype='application/json')

        return HttpResponse(books_json, content_type="application/json")
        # return HttpResponse(json.dumps(response_data), content_type="application/json")