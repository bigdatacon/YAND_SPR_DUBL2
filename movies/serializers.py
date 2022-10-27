from rest_framework import routers, serializers, viewsets
from .models import FilmWorkMovie, Genre, Person

# Serializers define the API representation.
#тут Важный вопрос что если добавить жанры то все падает

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'title', 'description']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'full_name']


class FilmWorkMovieSerializer(serializers.HyperlinkedModelSerializer):
    genres = GenreSerializer(many=True)
    persons = PersonSerializer(many=True)

    class Meta:
        model = FilmWorkMovie
        fields = ['id', 'title', 'description', 'rating', 'genres', 'persons']