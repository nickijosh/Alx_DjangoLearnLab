from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.db.models import Q
from django.contrib import messages

def list_books(request):
    query = request.GET.get("q", "").strip()
    books = Book.objects.all()

    # Secure search with input validation and ORM filtering
    if query:
        if len(query) > 100:
            messages.error(request, "Search query too long.")
        else:
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(summary__icontains=query)
            )

    return render(request, "bookshelf/book_list.html", {"books": books, "query": query})


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect("list_books")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form})


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect("list_books")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/form_example.html", {"form": form})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect("list_books")
    return render(request, "bookshelf/confirm_delete.html", {"book": book})
