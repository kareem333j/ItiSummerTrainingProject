from django.urls import path
from . import views

urlpatterns = [
    path('all', views.books, name='books'),
    path('all/<int:pk>/info', views.get_book, name='books.book'),
    path('categories', views.categories, name='categories'),
    path('categories/add', views.AddCategory.as_view(), name='categories.add'),
    path('categories/edit/<int:pk>', views.UpdateCategory.as_view(), name='categories.edit'),
    path('categories/delete/<int:pk>', views.delete_category, name='categories.delete'),
    path('borrowed', views.borrowed_books, name='books.borrowed'),
    path('add', views.AddBook.as_view(), name='books.add'),
    path('<int:pk>/edit', views.EditBook.as_view(), name='books.edit'),
    path('<int:pk>/delete', views.delete_book, name='books.delete'),
    path('<int:pk>/borrow', views.borrow, name='books.borrow'),
    path('<int:pk>/return', views.return_book, name='books.return'),
    path('search/books/<str:item>', views.search_books, name='books.search'),
    path('search/borrows/<str:item>', views.search_borrowed_books, name='books.search'),
]