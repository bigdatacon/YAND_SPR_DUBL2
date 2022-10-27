from rest_framework import routers, serializers, viewsets
from .models import FilmWorkMovie

# Serializers define the API representation.
class FilmWorkMovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilmWorkMovie
        fields = ['id', 'title', 'description', 'rating']