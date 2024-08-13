from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_books')
    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='my_books')
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)

    def __str__(self):
        return f'{self.id}: {self.name}'


class UserBookRelation(models.Model):
    rate_choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(null=True, choices=rate_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_rate = self.rate

    def save(self, *args, **kwargs):
        from store.logic import set_rate

        creating = not self.pk
        super().save(*args, **kwargs)
        new_rating = self.rate

        if new_rating != self.old_rate or creating:
            set_rate(self.book)
