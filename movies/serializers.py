from rest_framework import routers, serializers, viewsets
from .models import FilmWorkMovie

# Serializers define the API representation.
#тут Важный вопрос что если добавить жанры то все падает

class FilmWorkMovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilmWorkMovie
        fields = ['id', 'title', 'description', 'rating']