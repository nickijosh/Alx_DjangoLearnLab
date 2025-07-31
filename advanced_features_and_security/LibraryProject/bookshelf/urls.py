from django.urls import path
from . import views

urlpatterns = [
    path('form-example/', views.form_example_view, name='form_example'),
    path('books/', views.list_books, name='list_books'),  # existing view
]
