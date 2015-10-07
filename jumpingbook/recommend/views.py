import json
from braces.views import CsrfExemptMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View
from core.models import Book
from users.models import UserBookRating


class BookListView(CsrfExemptMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category-id','');
        page = request.POST.get('page', 1)
        already_rating_book_list = request.user.userbookrating_set.values_list('book_id', flat=True)
        if ( len(category_id) == 0 ):
            books = Book.objects.exclude(id__in=already_rating_book_list).values("id", "title", "image_url", "category__name", "author", "publisher", "published_date")
        else:
            books = Book.objects.filter(category__category__id=category_id).exclude(id__in=already_rating_book_list).values("id", "title", "image_url", "category__name", "author", "publisher", "published_date")

        # if ( len(category_id) == 0 ):
        #     books = Book.objects.exclude(id__in=already_rating_book_list).all()
        # else:
        #     books = Book.objects.filter(category__id=category_id).exclude(id__in=already_rating_book_list).all()



        paginator = Paginator(books, 12)
        current_page = paginator.page(page)

        data = {
            'next_page_num': current_page.next_page_number() if current_page.has_next() else -1,
            'items': list(current_page)
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")

class RatingBookView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item-id')
        rating = int(request.POST.get('rating'))

        try:
            user_book_rating, created = UserBookRating.objects.get_or_create(user=request.user, book=Book.objects.get(id=item_id),
                                                                             defaults={'score':rating})
            if not(created):
                user_book_rating.score = rating
                user_book_rating.save()
        except Exception as e:
            return HttpResponseBadRequest()

        return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json")

class RatedBookListView(CsrfExemptMixin, LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_book_ratings = request.user.userbookrating_set.select_related('book').all()
        rated_books = []
        for user_book_rating in user_book_ratings:
            book = user_book_rating.book
            rated_books.append({
                "id": book.id,
                "image_url": book.image_url,
                "title": book.title,
                "author": book.author,
                "publisher": book.publisher,
                "published_date": book.published_date,
                "score": user_book_rating.score
            })

        return HttpResponse(json.dumps(rated_books, cls=DjangoJSONEncoder), content_type="application/json")

class CancelRatingBookView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item-id')
        try:
            UserBookRating.objects.filter(user=request.user, book=Book.objects.get(id=item_id)).delete()
        except Exception as e:
            return HttpResponseBadRequest()

        return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json")