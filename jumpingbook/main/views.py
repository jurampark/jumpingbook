from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, View
from recommend.models import UserBookRating


class LoginView(TemplateView):
    template_name = "main/login.html"

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "main/index.html"

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "main/mypage.html"

class BookRatingView(LoginRequiredMixin, TemplateView):
    template_name = "main/book_rating.html"

class BookRecommendedView(LoginRequiredMixin, View):
    template_name = "main/book_recommended.html"

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                      {} )

    def post(self, request, *args, **kwargs):
        pass

        # Book.objects.values("id", "name", "author", "publisher", "published_date")

        # already_rating_book_list = request.user.userbookrating_set.values_list('book_id', flat=True)
        # books = Book.objects.exclude(id__in=already_rating_book_list).values("id", "name", "author", "publisher", "published_date")
        # return HttpResponse(json.dumps(list(books), cls=DjangoJSONEncoder), content_type="application/json")
        #
        # user_book_ratings = request.user.userbookrating_set.select_related('book').all()
        # rated_books = []
        # for user_book_rating in user_book_ratings:
        #     book = user_book_rating.book
        #     rated_books.append({
        #         "id": book.id,
        #         "name": book.name,
        #         "author": book.author,
        #         "publisher": book.publisher,
        #         "published_date": book.published_date,
        #         "score": user_book_rating.score
        #     })
        #
        # return HttpResponse(json.dumps(rated_books, cls=DjangoJSONEncoder), content_type="application/json")
        #
        # UserBookRating.objects