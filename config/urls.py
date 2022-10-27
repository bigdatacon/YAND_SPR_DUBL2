from django.contrib import admin
from django.urls import path
from movies import views

from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from movies.models import FilmWorkMovie
from movies.views import FilmWorkMovieViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'FilmWorkMovie', FilmWorkMovieViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('film_workmovie', views.index, name='film_workmovie'),

    path('', include(router.urls)),
    path('film_work_movie_view_set/', include('rest_framework.urls', namespace='rest_framework')),

    path('filmworkmovie_list/', views.filmworkmovie_list),
]
