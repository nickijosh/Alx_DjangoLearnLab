from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'isbn', 'summary']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'summary': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'isbn': 'ISBN Number',
        }
