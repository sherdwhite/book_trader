import logging
import random

from books.models import Book, Rating
from django.contrib.auth.models import User
from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate randomized ratings for all books and users (!! deletes all existing ratings !!)"

    def handle(self, *args, **options):
        Rating.objects.all().delete()
        for user in User.objects.all():
            for book in Book.objects.all():
                random_rating = random.randint(0, 5)
                rating = Rating.objects.create(
                    rating=random_rating,
                    user=user,
                    book=book,
                )
                print(f"Generated rating: {rating}")
