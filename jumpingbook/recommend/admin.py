from django.contrib import admin
from recommend.models import Category
from core.models import Book, Category

admin.site.register(Category)
admin.site.register(Book)