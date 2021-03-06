import json
from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum, Prefetch, Avg
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from django.views.generic import TemplateView, View, DetailView
import operator
from core.models import Book, Category, SubCategory, BookComments
from users.models import UserBookRating, UserFriend


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
    template_name = "users/mypage.html"

    def get_context_data(self, **kwargs):
        context = super(MyPageView, self).get_context_data(**kwargs)
        context['books'] = UserBookRating.objects.filter(user=self.request.user).select_related('book').values('book__id','book__title','book__author', 'book__publisher','book__published_date','score')
        context['friends'] = UserFriend.objects.filter(user=self.request.user).select_related('friend').values('friend__username', 'friend__first_name', 'friend__last_name', 'friend__email')

        print context['books']
        return context

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
                        if UserFriend.objects.filter(user=request.user, friend__id=other_rating.user_id).exists():
                            neighbors[other_rating.user_id] = 10
                        else:
                            neighbors[other_rating.user_id] = 1

            neighbors = sorted( neighbors.items(), key=operator.itemgetter(1), reverse=True)
            recommend_books = {}
            for neighbor in neighbors[:5]:
                neighbor_ratings = UserBookRating.objects.filter(user__id=neighbor[0]).filter(score__gte=7).all()
                for neighbor_rating in neighbor_ratings:
                    if recommend_books.has_key(neighbor_rating.book_id):
                        recommend_books[neighbor_rating.book_id] = recommend_books[neighbor_rating.book_id] + 1
                    else:
                        recommend_books[neighbor_rating.book_id] = 1

            recommend_books = sorted( recommend_books.items(), key=operator.itemgetter(1), reverse=True)

            for recommend_book in recommend_books:
                if not(UserBookRating.objects.filter(user=request.user, book__id=recommend_book[0]).exists()):
                    books.append( Book.objects.get(id=recommend_book[0]) )

        return render(request,
                      self.template_name,
                      {'rated_books_count':rated_books_count,
                       'books': books[:15]
                       } )

    def post(self, request, *args, **kwargs):
        pass

class BookSearchView(TemplateView):
    template_name = "main/book_search.html"

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query','')
        context = super(BookSearchView, self).get_context_data(**kwargs)
        context['books'] = Book.objects.filter(Q(title__icontains=query) |
                               Q(author__icontains=query)).all()[:15]
        return context

class BookDetailView(DetailView):

    template_name = "main/book_detail.html"
    model = Book
    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['evaluation_count'] = UserBookRating.objects.filter(book__id=self.kwargs['pk']).count()
        context['avg_star'] = UserBookRating.objects.filter(book__id=self.kwargs['pk']).aggregate(Avg('score'))['score__avg']
        rating = UserBookRating.objects.filter(user=self.request.user, book__id=self.kwargs['pk']).first()

        if rating is None:
            context['star'] = 0
        else:
            context['star'] = rating.score

        context['predict_star'] = 4.4
        return context


def getCommentList( book_id ):
    return HttpResponse(json.dumps(list(BookComments.objects.filter(book__id=book_id).values('user__username', 'comment')), cls=DjangoJSONEncoder), content_type="application/json")

class BookCommentView(View):

    def get(self, request, *args, **kwargs):
        return getCommentList(kwargs['pk'])

    def post(self, request, *args, **kwargs):
        BookComments.objects.create(user=request.user, book_id=kwargs['pk'], comment = request.POST.get('comment'))

        return getCommentList(kwargs['pk'])
        # return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json")

# class AddFriendView(TemplateView):
#
#
#     def get_context_data(self, **kwargs):
#         context = super(AddFriendView, self).get_context_data(**kwargs)
#         context['users'] = User.objects.exclude(username=self.request.user.username).all()
#
#         # print dir(context['users'][0])
#
#         return context

# class ScrapKyoboBookView(View):
#
#     template_name = "supervisor/scrapkyobobook.html"
#
#     def get(self, request, *args, **kwargs):
#
#         return render(request,
#                       self.template_name,
#                       {} )

class AddFriendView(LoginRequiredMixin, View):

    template_name = "main/add_friend.html"

    def get(self, request, *args, **kwargs):
        users = User.objects.exclude(username=self.request.user.username).values('id','username', 'last_name', 'first_name', 'email')

        for user in users:
            user['isFriend'] = UserFriend.objects.filter(user=self.request.user, friend_id=user['id']).exists()

        return render(request, self.template_name, {
            'users': users
        })

    def post(self, request, *args, **kwargs):
        UserFriend.objects.create( user = request.user, friend_id = request.POST.get('user-id'))

        return HttpResponse(json.dumps({}, cls=DjangoJSONEncoder), content_type="application/json")