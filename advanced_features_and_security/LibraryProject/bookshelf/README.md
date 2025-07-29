# Permissions and Groups Setup

## Groups:
- **Viewers**: can_view
- **Editors**: can_view, can_create, can_edit
- **Admins**: can_view, can_create, can_edit, can_delete

## Models
The `Book` model includes custom permissions in `Meta.permissions`.

## Setup Script
Run `python manage.py setup_groups` to initialize groups with correct permissions.

## Views
Permissions are enforced using `@permission_required` decorators on views such as:
- `list_books` requires `can_view`
- `add_book` requires `can_create`
- `edit_book` requires `can_edit`
- `delete_book` requires `can_delete`
