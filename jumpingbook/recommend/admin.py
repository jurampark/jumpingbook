from django.contrib import admin
from core.models import Book, Category

admin.site.register(Category)
admin.site.register(Book)