from django.contrib import admin
from .models import Category, SubCategory, Book

# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author')
#     search_fields = ['title']
#     # list_filter = ('title',)
#
# admin.site.register(Category)
# admin.site.register(SubCategory)
# admin.site.register(Book, BookAdmin)
from users.models import UserBookRating

admin.site.register(UserBookRating)