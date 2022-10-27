from django.contrib import admin
from .models import FilmWorkMovie



@admin.register(FilmWorkMovie)
class FilmworkAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating',)
    # порядок следования полей в форме создания/редактирования
    fields = (
        'title', 'type', 'description', 'creation_date',
        'rating',
    )