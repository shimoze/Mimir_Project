from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Genre
from .forms import BookForm
from django.http import HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.db.models import Q

from rest_framework import viewsets, permissions
from .serializers import GenreSerializer, BookSerializer
from .permissions import IsOwnerOrReadOnly

from .tasks import send_welcome_email

# Create your views here.
def book_list(request):
    search_query = request.GET.get('q', '').strip()
    genre_id = request.GET.get('genre')

    # 1. prefetch_related ускоряет загрузку жанров для списка книг
    books = Book.objects.all().prefetch_related('genres')

    # Поиск
    if search_query:
        words = search_query.split()
        q_filter = Q()
        for word in words:
            q_filter &= (
                Q(title__icontains=word) |
                Q(author__icontains=word) |
                Q(content__icontains=word)
            )
        books = books.filter(q_filter)

    # Фильтр по жанру
    # 2. Проверяем isdigit(), чтобы не было ошибки при вводе текста в URL
    if genre_id and genre_id.isdigit():
        books = books.filter(genres__id=genre_id)

    # 3. distinct() гарантирует, что книги не будут дублироваться в списке
    books = books.distinct()

    genres = Genre.objects.all()

    # Безопасно переводим в int для шаблона
    current_genre_id = int(genre_id) if genre_id and genre_id.isdigit() else None

    return render(request, 'library/book_list.html', {
        'books': books,
        'search_query': search_query,
        'genres': genres,
        'current_genre_id': current_genre_id,
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'library/book_detail.html', {'book': book})

@login_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()

    return render(request, 'library/book_form.html', {'form': form})

@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if book.owner != request.user:
        return HttpResponseForbidden("Вы не являетесь владельцем этой записи.")

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)
        
    else:
        form = BookForm(instance=book)
        
    return render(request, 'library/book_form.html', {'form': form})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if book.owner != request.user:
        return HttpResponseForbidden("Вы не являетесь владельцем этой записи.")

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    
    return render(request, 'library/book_confirm_delete.html', {'book':book})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            send_welcome_email.delay(user.username)

            return redirect('book_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
