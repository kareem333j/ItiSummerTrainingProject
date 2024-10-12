from django import forms
from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'description', 'stock', 'category', 'image')
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)