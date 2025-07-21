from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
print("Books by John Doe:")
author_name = "John Doe"
author = Author.objects.get(name=author_name)
books = Book.objects.filter(author=author)
for book in books:
    print("-", book.title)

# 2. List all books in a library
print("\nBooks in City Library:")
library_name = "City Library"
library = Library.objects.get(name=library_name)
for book in library.books.all():
    print("-", book.title)

# 3. Retrieve the librarian for a library
print("\nLibrarian of City Library:")
librarian = Librarian.objects.get(library__name="City Library")
print("-", librarian.name)
