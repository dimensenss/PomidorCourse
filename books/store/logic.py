from django.db.models import Avg

from store.models import UserBookRelation


def set_rate(book):
    avg_rating = UserBookRelation.objects.filter(book=book).aggregate(rating=Avg('rate')).get('rating')
    book.rating = avg_rating
    book.save()