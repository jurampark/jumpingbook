from braces.views import CsrfExemptMixin
from django.core.serializers import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View
from core.models import Book
from users.models import UserBookBlackList, UserBookWishList


class AddBookToBlackListView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item-id')

        try:
            user_book_black_list, created = UserBookBlackList.objects.get_or_create(user=request.user, book=Book.objects.get(id=item_id))
        except Exception as e:
            return HttpResponseBadRequest()

        return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json")

class AddBookToWishListView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item-id')

        try:
            user_book_wish_list, created = UserBookWishList.objects.get_or_create(user=request.user, book=Book.objects.get(id=item_id))
        except Exception as e:
            return HttpResponseBadRequest()

        return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json")