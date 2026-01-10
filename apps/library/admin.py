from django.contrib import admin
from .models import Book, Genre
# Register your models here.

admin.site.register(Genre)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','year')
    filter_horizontal = ('genres',)
    search_fields = ('title','author')