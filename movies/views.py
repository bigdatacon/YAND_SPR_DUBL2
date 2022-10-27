from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import FilmWorkMovie, GenreFilmWork, Genre, PersonFilmWork, Person
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import FilmWorkMovieSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


class FilmWorkMovieViewSet(viewsets.ModelViewSet):
    queryset = FilmWorkMovie.objects.all()
    serializer_class = FilmWorkMovieSerializer

@csrf_exempt
def filmworkmovie_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        filmworkmovie = FilmWorkMovie.objects.all()
        serializer = FilmWorkMovieSerializer(filmworkmovie, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FilmWorkMovieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# Create your views here.
def index(request):
    data = []
    for film in FilmWorkMovie.objects.all():
        film_info = {
            'uuid': film.id,
            'title': film.title,
            'description': film.description,
            'rating': film.rating,
            # 'genres': film.genres,
            # 'persons': film.persons,
        }
        # for genre in filmworks.genres.all()
        # for genre in name.filmworks.all():
        #     film_info['files'].append(furl.file_path.url)
        data.append(film_info)
    return JsonResponse({'results': data})