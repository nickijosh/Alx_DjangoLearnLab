from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create groups and assign permissions'

    def handle(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(Book)

        permissions = {
            'can_view': Permission.objects.get(codename='can_view'),
            'can_create': Permission.objects.get(codename='can_create'),
            'can_edit': Permission.objects.get(codename='can_edit'),
            'can_delete': Permission.objects.get(codename='can_delete'),
        }

        groups = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        for group_name, perms in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm in perms:
                group.permissions.add(permissions[perm])
            self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' configured."))
