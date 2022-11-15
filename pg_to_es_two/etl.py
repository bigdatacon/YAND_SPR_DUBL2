import time
from pg_to_es_persons import PGtoESPersons
from pg_to_es_films import PGtoESFilms

persons = PGtoESPersons()
films = PGtoESFilms()

"""1. быстрое удаление индекса для проверки - потом удалить для персон """
# index_name = 'persons_test'
# print(f' eto persons.del_index(index_name) : {persons.del_index(index_name)}')
# print(f' eto personsle.read_index(index_name) : {persons.read_index(index_name)}')

"""2 быстрое удаление индекса для проверки - потом удалить для фильмов """
# index_name = 'films_test'
# print(f' eto films.del_index(index_name) : {films.del_index(index_name)}')
# print(f' eto films.read_index(index_name) : {films.read_index(index_name)}')

while True:
    persons.sync_persons_changes()
    time.sleep(3)
    films.sync_films_changes()
    time.sleep(3)