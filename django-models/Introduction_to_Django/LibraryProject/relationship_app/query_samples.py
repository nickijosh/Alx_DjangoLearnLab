import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# 1. Ensure author exists (or create)
author_name = "Chinua Achebe"
author, created = Author.objects.get_or_create(name=author_name)

# Create a book for that author if none exists
if not Book.objects.filter(author=author).exists():
    Book.objects.create(title="Things Fall Apart", author=author)

books_by_author = Book.objects.filter(author=author)
print(f"Books by {author.name}: {[book.title for book in books_by_author]}")

# 2. Ensure library exists (or create)
library_name = "National Library"
library, created = Library.objects.get_or_create(name=library_name)

# Link book to library if not already linked
for book in books_by_author:
    library.books.add(book)

books_in_library = library.books.all()
print(f"Books in {library.name}: {[book.title for book in books_in_library]}")

# 3. Ensure librarian exists for the library (or create)
librarian, created = Librarian.objects.get_or_create(name="Grace Okonkwo", library=library)
print(f"Librarian of {library.name}: {librarian.name}")
