from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import  reverse

class Category(models.Model):
    title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.title
    
class Book(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to='books', null=True)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    
    @property
    def book_url(self):
        url = reverse('students.show', args=[self.id])
        return url
    
    @property
    def image_url(self):
        return f'/media/{self.image}'
    
    def __str__(self):
        return self.title
    
class Borrow(models.Model):
    user = models.ForeignKey(User, related_name='borrowed_user', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='book', on_delete=models.CASCADE)
    borrowed_dt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} borrow {self.book.title}'