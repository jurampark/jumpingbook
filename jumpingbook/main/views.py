from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum, Prefetch
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, View
import operator
from core.models import Book, Category, SubCategory
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


        books = []

        if rated_books_count >= 20:
            ratings = request.user.userbookrating_set.all()
            neighbors = {}
            for rating in ratings:
                book = rating.book
                score = rating.score
                other_ratings = UserBookRating.objects.filter(book=book).filter(score__gte=score-3).filter(score__lte=score+3).exclude(user=request.user).all()
                for other_rating in other_ratings:
                    if neighbors.has_key(other_rating.user_id):
                        neighbors[other_rating.user_id] = neighbors[other_rating.user_id]+1
                    else:
                        neighbors[other_rating.user_id] = 1

            neighbors = sorted( neighbors.items(), key=operator.itemgetter(1), reverse=True)
            recommend_books = {}
            for neighbor in neighbors[:5]:
                neighbor_ratings = UserBookRating.objects.filter(user__id=neighbor[0]).order_by('-score').all()
                for neighbor_rating in neighbor_ratings:
                    if recommend_books.has_key(neighbor_rating.book_id):
                        recommend_books[neighbor_rating.book_id] = recommend_books[neighbor_rating.book_id] + 1
                    else:
                        recommend_books[neighbor_rating.book_id] = 1

            recommend_books = sorted( recommend_books.items(), key=operator.itemgetter(1), reverse=True)


            for recommend_books in recommend_books[:12]:
                books.append( Book.objects.get(id=recommend_books[0]) )

        return render(request,
                      self.template_name,
                      {'rated_books_count':rated_books_count,
                       'books': books
                       } )

    def post(self, request, *args, **kwargs):
        pass

class BookSearchView(TemplateView):
    template_name = "main/book_search.html"

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query','')
        context = super(BookSearchView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.filter(title__contains=query).all()[:12]
        return context