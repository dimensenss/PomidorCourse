from django.contrib import admin
from store.models import Book, UserBookRelation


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


@admin.register(UserBookRelation)
class UserBookRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book')