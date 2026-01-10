from django import forms
from .models import Book, Genre

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'year', 'content', 'cover', 'genres')

    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required= False
    )