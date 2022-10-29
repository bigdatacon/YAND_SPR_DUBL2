from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import FilmWorkMovie, GenreFilmWork, Genre, PersonFilmWork, Person
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import FilmWorkMovieSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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


#вот здесь пример с теорие https://www.django-rest-framework.org/tutorial/3-class-based-views/

class MovieList(APIView):
    permission_classes = [permissions.AllowAny]
    """
    List all movies, or create a new snippet.
    """
    # def get(self, request, format=None):
    #     filmworkmovie = FilmWorkMovie.objects.all()
    #     serializer = FilmWorkMovieSerializer(filmworkmovie, many=True)
    #     return Response(serializer.data)

    def get(self, request, format=None):
        if request.method == 'GET' and 'min_rating' in request.GET:
            # Параметр min_rating был передан
            min_rating = float(request.GET['min_rating'])
            filmworkmovie = FilmWorkMovie.objects.filter(rating__gte=min_rating)
            serializer = FilmWorkMovieSerializer(filmworkmovie, many=True)
            return Response(serializer.data)
        elif request.method == 'GET' and 'actor' in request.GET:
            # Параметр min_rating был передан
            actor =  Person.objects.get(full_name=request.GET['actor'])
            filmworkmovie =  actor.filmworks.all()
            # filmworkmovie = FilmWorkMovie.persons.filmworks.filter(persons.filmworks__contains = actor)
            serializer = FilmWorkMovieSerializer(filmworkmovie, many=True)
            return Response(serializer.data)
            # return Response([film.title for film in actor.filmworks.all()])

        elif request.method == 'GET' and 'genre' in request.GET:
            # Параметр min_rating был передан
            actor =  Genre.objects.get(name=request.GET['genre'])
            filmworkmovie =  actor.filmworks.all()
            # filmworkmovie = FilmWorkMovie.persons.filmworks.filter(persons.filmworks__contains = actor)
            serializer = FilmWorkMovieSerializer(filmworkmovie, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = FilmWorkMovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def return_films_rating_over(self, request, format=None):
    #     if request.method == 'GET' and request.min_rating:
    #         filmworkmovie = FilmWorkMovie.objects.filter(rating__gte=request.data)
    #         serializer = FilmWorkMovieSerializer(filmworkmovie, many=True)
    #         return Response(serializer.data)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)





# Create your views here.
def index(request):
    data = []
    for film in FilmWorkMovie.objects.all():
        film_info = {
            'uuid': film.id,
            'title': film.title,
            'description': film.description,
            'rating': film.rating,
            'genres': [{'id': genre.id, 'name': genre.name} for genre in film.genres.all()],
            'persons': [{'id': person.id,  'full_name': person.full_name} for person in film.persons.all()]
            # 'genres': film.genres,
            # 'persons': film.persons,
        }
        # for genre in filmworks.genres.all()
        # for genre in name.filmworks.all():
        #     film_info['files'].append(furl.file_path.url)

        # 'genres': [{'id': genre.id, 'name': genre.name} for genre in film.genres.all()]
        data.append(film_info)
    return JsonResponse({'results': data})