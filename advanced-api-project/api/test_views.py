from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client = APIClient()
        self.client.login(username="testuser", password="password123")

        # Create test books
        self.book1 = Book.objects.create(title="Django Basics", author="John Doe", publication_year=2022)
        self.book2 = Book.objects.create(title="Advanced Python", author="Jane Smith", publication_year=2021)
        self.book3 = Book.objects.create(title="Django REST Framework", author="John Doe", publication_year=2020)

        # URL patterns (these should match names in your urls.py)
        self.list_url = reverse("book-list")  # GET/POST
        self.detail_url = lambda pk: reverse("book-detail", kwargs={"pk": pk})  # GET/PUT/DELETE

    # --- CRUD Tests ---
    def test_create_book(self):
        data = {"title": "New Book", "author": "New Author", "publication_year": 2023}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_get_book_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_book_detail(self):
        response = self.client.get(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Django Basics")

    def test_update_book(self):
        data = {"title": "Updated Title", "author": "John Doe", "publication_year": 2022}
        response = self.client.put(self.detail_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # --- Filtering, Searching, Ordering ---
    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url + "?author=John Doe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url + "?search=Django")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Django" in book["title"] for book in response.data))

    def test_order_books_by_publication_year(self):
        response = self.client.get(self.list_url + "?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))

    # --- Permissions ---
    def test_permission_required_for_post(self):
        self.client.logout()
        data = {"title": "No Auth", "author": "None", "publication_year": 2020}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
