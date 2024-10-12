from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import *
from django.views import generic
from .forms import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q

@login_required
def books(request):
    All_books = Book.objects.all()
    borrowed_books = Borrow.objects.filter(user=request.user)
    for book in All_books:
        for i in borrowed_books:
            if i.book.id == book.id:
                book.borrowed = True
                break
            else:
                book.borrowed = False
    
    return render(request, 'books/all-books.html',{'books':All_books, 'borrowed_books':borrowed_books,'borrowed_length':borrowed_books.count()-1})

@login_required
def get_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    borrowed_books = Borrow.objects.filter(user=request.user)
    for i in borrowed_books:
        if i.book.id == book.id:
            book.borrowed = True
            break
        else:
            book.borrowed = False
    
    return render(request, 'books/info.html', {'book':book})

@login_required
def categories(request):
    if request.user.is_superuser:
        all_categories = Category.objects.all()
        return render(request, 'books/categories.html', {'categories':all_categories})
    return redirect('main')

class AddCategory(LoginRequiredMixin, UserPassesTestMixin,generic.CreateView):
    template_name = 'books/add-category.html'
    form_class = CategoryForm
    success_url = '/books/categories'
    
    def test_func(self):
        return self.request.user.is_superuser
    
class UpdateCategory(LoginRequiredMixin, UserPassesTestMixin,generic.UpdateView):
    template_name = 'books/update-category.html'
    form_class = CategoryForm
    success_url = '/books/categories'
    queryset = Category.objects.all()
    pk_url_kwarg = 'pk'
    
    def test_func(self):
        return self.request.user.is_superuser

@login_required
def delete_category(request, pk):
    if request.user.is_superuser:
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Category deleted successfully.!')
        return redirect(reverse('categories'))
    return redirect('main')

def borrowed_books(request):
    books = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            books = Borrow.objects.all()
        else:
            books = Borrow.objects.filter(user=request.user)
        return render(request, 'books/borrowed-books.html', {'books':books})
    else:
        return redirect('home')

@login_required
def borrow(request, pk):
    user = request.user
    book = get_object_or_404(Book, pk=pk)
    
    borrow_process = Borrow.objects.create(
        user=user,
        book=book,
    )
    
    if borrow_process:
        book.stock -= 1
        book.save()
        messages.success(request, f'Congrats, you borrowed "{book.title}" book.!')
        
    url  = reverse("books")
    return  redirect(url)

@login_required
def return_book(request, pk):
    user = request.user
    book = get_object_or_404(Book, pk=pk)
    
    return_book = get_object_or_404(Borrow, user=user, book=book)
    
    if return_book:
        return_book.delete()
        book.stock += 1
        book.save()
        messages.success(request, f'Book returned successfully.!')
        
    url  = reverse("books")
    return  redirect(url)
        
    
    
class AddBook(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    form_class = BookForm
    template_name = 'books/add.html'
    success_url = '/books/all'
    
    def test_func(self):
        return self.request.user.is_superuser
    
class EditBook(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    form_class = BookForm
    template_name = 'books/edit.html'
    success_url = '/books/all'
    queryset = Book.objects.all()
    pk_url_kwarg = 'pk'
    
    def test_func(self):
        return self.request.user.is_superuser

@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    url  = reverse("books")
    messages.success(request,'Book deleted successfully.!')
    return  redirect(url)

@login_required
def search_books(request, item):
    if item == "null":
        books = Book.objects.all()
    else:
        books = Book.objects.filter(
            Q(title__contains=item)
        )
        
        
    books_list = []
    for book in books:
        book_serializer = {
            'id': book.id,
            'image': book.image_url,
            'title': book.title,
            'author': book.author.username,
            'description': book.description,
            'category': book.category.title,
            'stock': book.stock,
        }
        borrowed_books = Borrow.objects.filter(user=request.user)
        for book in borrowed_books:
            if book.book.id == book_serializer['id']:
                book_serializer['borrowed'] = True
                break
            else:
                book_serializer['borrowed'] = False
        books_list.append(book_serializer)
        
    data = {
        'books': books_list
    }
    return JsonResponse(data, safe=False)


@login_required
def search_borrowed_books(request, item):
    if item == "null":
        if request.user.is_superuser:
            borrowed_books = Borrow.objects.all()
        else:
            borrowed_books = Borrow.objects.filter(user=request.user)
    else:
        if request.user.is_superuser:
            borrowed_books = Borrow.objects.filter(
                Q(book__title__contains=item)
            )
        else:
            borrowed_books = Borrow.objects.filter(
                Q(book__title__contains=item)
            ).filter(user=request.user)
        
    books_list = []
    for book in borrowed_books:
        book_serializer = {
            'id': book.book.id,
            'image': book.book.image_url,
            'title': book.book.title,
            'category': book.book.category.title,
            'borrowed_dt': book.borrowed_dt,
            'user': book.user.username,
            'user_id': book.user.pk,
        }
        books_list.append(book_serializer)
    
    data = {
        'books': books_list
    }
    return JsonResponse(data, safe=False)