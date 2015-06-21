from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum, Prefetch
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, View
from core.models import Book, Category
from users.models import UserBookRating


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

class BookSearchView(TemplateView):
    template_name = "main/book_search.html"

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query','')
        context = super(BookSearchView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.filter(name__contains=query).all()
        print context['books']
        return context