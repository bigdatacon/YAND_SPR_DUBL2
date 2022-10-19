import uuid
# https://www.youtube.com/watch?v=fsVY66QBhwM
from django.db import models
import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _




class Fileupl(TimeStampedModel):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    file_path = models.FileField(_('File'), upload_to='files/')
    resolution = models.CharField(_('Resolution'), null=True, max_length=100)
    codec_name = models.CharField(_('Codec'), max_length=100, null=True, blank=True)
    display_aspect_ratio = models.CharField(_('Display Aspect Ratio'), max_length=100, null=True, blank=True)
    fps = models.IntegerField(_('FPS'), null=True, blank=True)
    film = models.ForeignKey('FilmWork',  related_name='files', null=True, verbose_name="Фильм", on_delete=models.CASCADE)
    #
    class Meta:
        verbose_name = _('Fileupl')
        verbose_name_plural = _('Fileupl')
        # managed = False
        # db_table = f'"content"."file"'
        ordering = ["file_path"]
    #
    def __str__(self):
        return f'{self.file_path}'

class FilmWork(TimeStampedModel):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Name'), max_length=255, null=True,)
    certificate = models.TextField(_('Certificate'), blank=True)
    file_path = models.FileField(_('Original file'), upload_to='film_works/')
    # files = models.ManyToManyField('Fileupl', through='FileFilmWork', related_name='filmworks')

    class Meta:
        verbose_name = _('Film')
        verbose_name_plural = _('Films')
        # managed = False
        # db_table = f'"content"."film_work"'
        ordering = ["title"]

    def __str__(self):
        return f'{self.file_path}'

"""модели для базы фильмов из sqlite"""

class Gender(models.TextChoices):
    MALE = 'male', _('мужской')
    FEMALE = 'female', _('женский')


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')
        db_table = "genre"
        managed = False

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(_('имя'), max_length=50)
    birth_date = models.DateTimeField(_('дата рождения'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Персона')
        verbose_name_plural = _('Персоны')
        db_table = "person"
        managed = False

    def __str__(self):
        return f"{self.full_name}"


class GenreFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('FilmWorkMovie', on_delete=models.CASCADE, default=None)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "genre_film_work"
        verbose_name = _('Жанр кинопроизведения')
        verbose_name_plural = _('Жанры кинопроизведения')
        managed = False

    def __str__(self):
        return f"{self.film_work_id} - {self.genre_id}"





class PersonFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('FilmWorkMovie', on_delete=models.CASCADE, default=None)
    person = models.ForeignKey('Person', on_delete=models.CASCADE, default=None)
    role = models.CharField(_('роль'), max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "person_film_work"
        verbose_name = _('Участник кинопроизведения')
        verbose_name_plural = _('Участники кинопроизведения')
        managed = False

    def __str__(self):
        return f"{self.role}"


class FilmWorkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV Show')



class FilmWorkMovie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'), blank=True, null=True)
    creation_date = models.DateField(_('Дата создания'), blank=True, null=True)
    file_path = models.FileField(_('Путь к файлу'), upload_to='film_works/')
    rating = models.FloatField(
        _('Рейтинг'),
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        blank=True, null=True
    )
    type = models.CharField(_('Тип'), max_length=20, choices=FilmWorkType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # genres = models.ManyToManyField(Genre, through='GenreFilmWork', verbose_name=_('Жанры'))
    # person = models.ManyToManyField(Person, through='PersonFilmWork', verbose_name=_('Персоны'))
    genres = models.ManyToManyField(Genre, through='GenreFilmWork', verbose_name=_('Жанры'), related_name='filmworks')
    persons = models.ManyToManyField(Person, through='PersonFilmWork', verbose_name=_('Персоны'), related_name='filmworks')

    class Meta:
        verbose_name = _('Кинопроизведение')
        verbose_name_plural = _('Кинопроизведения')
        db_table = "film_workmovie"
        managed = False
