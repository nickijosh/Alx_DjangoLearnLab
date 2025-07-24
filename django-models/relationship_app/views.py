from django.shortcuts import render
from .models import Book

# Function-Based View to list all books
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'list_books.html', {'books': books})

from django.views.generic.detail import DetailView
from .models import Library

# Class-Based View to show library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
