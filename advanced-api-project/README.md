# API View Documentation

This project demonstrates the use of Django REST Framework generic views for handling CRUD operations on the Book model.

## Endpoints

| Endpoint                 | Method | Description           | Permissions         |
|--------------------------|--------|------------------------|----------------------|
| /api/books/              | GET    | List all books         | Public               |
| /api/books/<id>/         | GET    | Retrieve a book        | Public               |
| /api/books/create/       | POST   | Create a new book      | Authenticated users  |
| /api/books/<id>/update/  | PUT    | Update a book          | Authenticated users  |
| /api/books/<id>/delete/  | DELETE | Delete a book          | Authenticated users  |

## View Customization

- `BookCreateView` and `BookUpdateView` override `perform_create` and `perform_update` for extended behavior.
- Permission classes ensure that only authenticated users can modify data.
