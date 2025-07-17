# encoding: utf-8

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField("Author", related_name="books")
    description = models.TextField(blank=True)
    publisher = models.ForeignKey("Publisher", on_delete=models.CASCADE)
    isbn = models.CharField(max_length=255, unique=True, help_text="ISBN-10 or ISBN-13")

    # Book Details
    publication_date = models.DateField(blank=True, null=True)
    page_count = models.PositiveIntegerField(blank=True, null=True)
    language = models.CharField(
        max_length=10, default="en", help_text="Language code (e.g., en, es, fr)"
    )

    # Categories
    GENRE_CHOICES = [
        ("fiction", "Fiction"),
        ("non_fiction", "Non-Fiction"),
        ("mystery", "Mystery"),
        ("romance", "Romance"),
        ("sci_fi", "Science Fiction"),
        ("fantasy", "Fantasy"),
        ("biography", "Biography"),
        ("history", "History"),
        ("self_help", "Self Help"),
        ("business", "Business"),
        ("textbook", "Textbook"),
        ("children", "Children"),
        ("young_adult", "Young Adult"),
        ("other", "Other"),
    ]
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default="other")

    # Ratings
    average_rating = models.DecimalField(
        decimal_places=1,
        max_digits=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    # Market Info
    original_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Original retail price",
    )

    # Images
    cover_image = models.ImageField(upload_to="book_covers/", blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("title",)
        indexes = [
            models.Index(fields=["isbn"]),
            models.Index(fields=["genre"]),
        ]

    def __str__(self):
        return self.title

    @property
    def author_names(self):
        """Get comma-separated list of author names"""
        return ", ".join([author.name for author in self.authors.all()])


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(blank=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Rating(models.Model):
    rating = models.IntegerField(
        default=3, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    user = models.ForeignKey(
        "auth.User",
        related_name="book_ratings",
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        "Book",
        related_name="ratings",
        on_delete=models.CASCADE,
    )
    review = models.TextField(blank=True, help_text="Optional written review")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "book"]
        ordering = ["-created_at"]

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


class BookCondition(models.Model):
    """Track specific copies of books and their condition"""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    owner = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="owned_books"
    )

    CONDITION_CHOICES = [
        ("new", "New"),
        ("like_new", "Like New"),
        ("very_good", "Very Good"),
        ("good", "Good"),
        ("acceptable", "Acceptable"),
        ("poor", "Poor"),
    ]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    condition_notes = models.TextField(blank=True)

    # Acquisition info
    acquired_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )

    # Availability
    is_available_for_trade = models.BooleanField(default=False)
    is_available_for_auction = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["book", "owner"]

    def __str__(self):
        return f"{self.book.title} ({self.get_condition_display()}) - {self.owner.username}"
