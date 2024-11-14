# encoding: utf-8
from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("Author", related_name="books")
    description = models.TextField(blank=True)
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE)
    isbn = models.CharField(max_length=255)
    average_rating = models.DecimalField(
        decimal_places=1,
        max_digits=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Rating(models.Model):
    rating = models.IntegerField(
        default=3, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        "auth.User",
        related_name="ratings",
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        "Book",
        related_name="ratings",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.rating} - {self.book.title} by {self.user.username}"

    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)
        book_id = self.book.id
        rating_average = (
            Rating.objects.filter(book_id=book_id)
            .aggregate(Avg("rating"))
            .get("rating__avg")
        )
        book = Book.objects.get(id=book_id)
        if rating_average and book:
            book.average_rating = round(rating_average, 1)
        else:
            book.average_rating = 0
        book.save()
