from django.contrib import admin
from users.models import UserBookRating

# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author')
#     search_fields = ['title']
#     # list_filter = ('title',)
#
# admin.site.register(Category)
# admin.site.register(SubCategory)
# admin.site.register(Book, BookAdmin)


admin.site.register(UserBookRating)