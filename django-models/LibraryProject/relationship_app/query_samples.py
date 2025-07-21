# query_samples.py

from relationship_app.models import Book, Library, Librarian

# 1. Query all books by a specific author
print("Books by John Doe:")
books = Book.objects.filter(author__name="John Doe")
for book in books:
    print("-", book.title)

# 2. List all books in a library
print("\nBooks in City Library:")
try:
    library_name = "City Library"
    library = Library.objects.get(name=library_name)
    for book in library.books.all():
        print("-", book.title)
except Library.DoesNotExist:
    print("Library not found.")

# 3. Retrieve the librarian for a library
print("\nLibrarian of City Library:")
try:
    librarian = Librarian.objects.get(library__name="City Library")
    print("-", librarian.name)
except Librarian.DoesNotExist:
    print("Librarian not found.")
