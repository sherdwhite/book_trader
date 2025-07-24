# -*- coding: utf-8 -*-

import asyncio

from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Author, Book, Publisher


class MainView(generic.TemplateView):
    template_name = "main.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context.update({"base_api_url": self.request.build_absolute_uri("/api")})

        return context


async def book_list_view(request):
    """Async view to list books with search and filtering"""
    search_query = request.GET.get("search", "")
    author_filter = request.GET.get("author", "")
    publisher_filter = request.GET.get("publisher", "")
    min_rating = request.GET.get("min_rating", "")
    page = request.GET.get("page", 1)

    # Build the query asynchronously
    books_queryset = Book.objects.select_related("publisher").prefetch_related(
        "authors", "ratings"
    )

    # Apply search filters
    if search_query:
        books_queryset = books_queryset.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(authors__name__icontains=search_query)
        ).distinct()

    if author_filter:
        books_queryset = books_queryset.filter(authors__name__icontains=author_filter)

    if publisher_filter:
        books_queryset = books_queryset.filter(
            publisher__name__icontains=publisher_filter
        )

    if min_rating:
        try:
            min_rating_float = float(min_rating)
            books_queryset = books_queryset.annotate(
                avg_rating=Avg("ratings__rating")
            ).filter(avg_rating__gte=min_rating_float)
        except ValueError:
            pass  # Invalid rating filter, ignore

    # Get books with async database operations
    books_list = await sync_to_async(list)(
        books_queryset.annotate(
            avg_rating=Avg("ratings__rating"), rating_count=Count("ratings")
        )
    )

    # Paginate results
    paginator = Paginator(books_list, 12)  # 12 books per page
    books_page = await sync_to_async(paginator.get_page)(page)

    # Get filter options for dropdowns
    authors_list = await sync_to_async(list)(
        Author.objects.values("name").distinct().order_by("name")
    )
    publishers_list = await sync_to_async(list)(
        Publisher.objects.values("name").distinct().order_by("name")
    )

    context = {
        "books": books_page,
        "search_query": search_query,
        "author_filter": author_filter,
        "publisher_filter": publisher_filter,
        "min_rating": min_rating,
        "authors": authors_list,
        "publishers": publishers_list,
        "page_obj": books_page,
    }

    return await sync_to_async(render)(request, "books/book_list.html", context)


async def book_detail_view(request, book_id):
    """Async view to display book details"""
    # Get book with related data
    book = await sync_to_async(get_object_or_404)(
        Book.objects.select_related("publisher").prefetch_related("authors", "ratings"),
        pk=book_id,
    )

    # Get average rating and rating count concurrently
    avg_rating_task = sync_to_async(book.ratings.aggregate(avg_rating=Avg("rating")))()
    rating_count_task = sync_to_async(book.ratings.count)()

    # Wait for both operations to complete
    avg_rating_result, rating_count = await asyncio.gather(
        avg_rating_task, rating_count_task
    )

    avg_rating = avg_rating_result.get("avg_rating")

    # Get related books by same authors (async)
    author_ids = await sync_to_async(list)(book.authors.values_list("id", flat=True))
    related_books = await sync_to_async(list)(
        Book.objects.filter(authors__in=author_ids).exclude(pk=book_id).distinct()[:5]
    )

    context = {
        "book": book,
        "avg_rating": avg_rating,
        "rating_count": rating_count,
        "related_books": related_books,
    }

    return await sync_to_async(render)(request, "books/book_detail.html", context)


async def author_books_view(request, author_id):
    """Async view to display all books by a specific author"""
    author = await sync_to_async(get_object_or_404)(Author, pk=author_id)

    # Get author's books with ratings
    books_queryset = Book.objects.filter(authors=author).select_related("publisher")
    books_list = await sync_to_async(list)(
        books_queryset.annotate(
            avg_rating=Avg("ratings__rating"), rating_count=Count("ratings")
        )
    )

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(books_list, 12)
    books_page = await sync_to_async(paginator.get_page)(page)

    context = {
        "author": author,
        "books": books_page,
        "page_obj": books_page,
    }

    return await sync_to_async(render)(request, "books/author_books.html", context)


async def search_suggestions_view(request):
    """Async AJAX endpoint for search suggestions"""
    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return JsonResponse({"suggestions": []})

    # Search for books and authors concurrently
    book_suggestions_task = sync_to_async(list)(
        Book.objects.filter(title__icontains=query).values("id", "title")[:5]
    )

    author_suggestions_task = sync_to_async(list)(
        Author.objects.filter(name__icontains=query).values("id", "name")[:5]
    )

    # Wait for both searches to complete
    book_suggestions, author_suggestions = await asyncio.gather(
        book_suggestions_task, author_suggestions_task
    )

    suggestions = []

    # Format book suggestions
    for book in book_suggestions:
        suggestions.append(
            {
                "type": "book",
                "id": book["id"],
                "title": book["title"],
                "url": f'/books/{book["id"]}/',
            }
        )

    # Format author suggestions
    for author in author_suggestions:
        suggestions.append(
            {
                "type": "author",
                "id": author["id"],
                "name": author["name"],
                "url": f'/authors/{author["id"]}/',
            }
        )

    return JsonResponse({"suggestions": suggestions})
