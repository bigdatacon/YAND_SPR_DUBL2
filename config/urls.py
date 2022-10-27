from django.contrib import admin
from django.urls import path
from movies import views

from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from movies.models import FilmWorkMovie

# Serializers define the API representation.
class FilmWorkMovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilmWorkMovie
        fields = ['id', 'title', 'description', 'rating']

# ViewSets define the view behavior.
class FilmWorkMovieViewSet(viewsets.ModelViewSet):
    queryset = FilmWorkMovie.objects.all()
    serializer_class = FilmWorkMovieSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'FilmWorkMovie', FilmWorkMovieViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),

]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('film_workmovie', views.index, name='film_workmovie'),

    path('', include(router.urls)),
    path('film_work_movie_view_set/', include('rest_framework.urls', namespace='rest_framework'))
]
