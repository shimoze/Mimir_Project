from rest_framework import serializers
from .models import Book, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many= True, read_only = True)

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Book
        fields = '__all__'