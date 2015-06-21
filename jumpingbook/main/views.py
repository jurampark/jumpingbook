from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum, Prefetch
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, View
from recommend.models import UserBookRating, Category, Book

class BookSearchView(TemplateView):
    template_name = "main/search.html"

class LoginView(TemplateView):
    template_name = "main/login.html"

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['book_count'] = Book.objects.count()
        context['rating_count'] = UserBookRating.objects.count()
        return context

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "main/mypage.html"

class BookRatingView(LoginRequiredMixin, TemplateView):
    template_name = "main/book_rating.html"

    def get_context_data(self, **kwargs):
        context = super(BookRatingView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class BookRecommendedView(LoginRequiredMixin, View):
    template_name = "main/book_recommended.html"

    def get(self, request, *args, **kwargs):

        rated_books_count = request.user.userbookrating_set.count()

        book_list = []
        if rated_books_count >= 10:
            books = Book.objects.prefetch_related(Prefetch('userbookrating_set')).all()
            for book in books[:10]:
                score = book.userbookrating_set.aggregate(Sum('score'))['score__sum']
                if score is None:
                    score = 0

                book_item = {
                    'book': book,
                    'score': score
                }

                book_list.append(book_item)

            book_list = sorted(book_list, key=lambda book: book['score'], reverse=True)

        return render(request,
                      self.template_name,
                      {'rated_books_count':rated_books_count,
                       'books': book_list[:10]
                       } )

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
