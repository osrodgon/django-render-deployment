from django.urls import path
from .views import BooksView

urlpatterns = [
    path('', BooksView.booksList, name="books-list"),
    path('create', BooksView.booksCreate, name="books-create"),
    path('<int:pk>', BooksView.booksDetail, name="books-detail"),
]