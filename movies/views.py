from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import FilmWorkMovie, GenreFilmWork, Genre, PersonFilmWork, Person
from rest_framework import viewsets
from rest_framework import permissions



# Create your views here.
def index(request):
    data = []
    for film in FilmWorkMovie.objects.all():
        film_info = {
            'uuid': film.id,
            'title': film.title,
            'description': film.description,
            'rating': film.rating,
            'genres': film.genres,
            # 'persons': film.persons,
        }
        for furl in name.filmworks.all():
            film_info['files'].append(furl.file_path.url)
        data.append(film_info)
    return JsonResponse({'results': data})