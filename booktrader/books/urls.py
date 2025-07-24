from django.urls import path

from . import views

app_name = "books"

urlpatterns = [
    path("", views.book_list_view, name="book_list"),
    path("<int:book_id>/", views.book_detail_view, name="book_detail"),
    path("authors/<int:author_id>/", views.author_books_view, name="author_books"),
    path(
        "search-suggestions/", views.search_suggestions_view, name="search_suggestions"
    ),
]
