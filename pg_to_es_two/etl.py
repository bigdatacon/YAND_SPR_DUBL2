import time
import logging
from pg_to_es_persons import PGtoESPersons
from pg_to_es_films import PGtoESFilms
from pg_to_es_genres import PGtoESGenres

logging_level = logging.DEBUG
main_logger = logging.getLogger()
main_logger.setLevel(logging_level)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging_level)
formatter = logging.Formatter("'%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler.setFormatter(formatter)

main_logger.addHandler(stream_handler)


"""1. быстрое удаление индекса для проверки - потом удалить для персон """
# index_name = 'persons_test'
# print(f' eto personsle.read_index(index_name) : {persons.read_index(index_name)}')
# print(f' eto persons.del_index(index_name) : {persons.del_index(index_name)}')

"""2 быстрое удаление индекса для проверки - потом удалить для фильмов """
# index_name = 'films_test'
# print(f' eto films.read_index(index_name) : {films.read_index(index_name)}')
# print(f' eto films.del_index(index_name) : {films.del_index(index_name)}')

"""3 быстрое удаление индекса для проверки - потом удалить для жанров """
# index_name = 'genres_test'
# print(f' eto genres.read_index(index_name) : {genres.read_index(index_name)}')
# print(f' eto genres.del_index(index_name) : {genres.del_index(index_name)}')

# persons = PGtoESPersons()
# films = PGtoESFilms()
# genres = PGtoESGenres()
# while True:
#     persons.sync_persons_changes()
#     time.sleep(3)
#     films.sync_films_changes()
#     time.sleep(3)
#     genres.sync_genres_changes()
#     time.sleep(2)


def do_etl():
    # main_logger.debug("Start loading from PostgreSQL to Elasticsearch")
    persons = PGtoESPersons()
    films = PGtoESFilms()
    genres = PGtoESGenres()
    main_logger.debug("Start loading from PostgreSQL to Elasticsearch")
    while True:
        persons.sync_persons_changes()
        time.sleep(3)
        films.sync_films_changes()
        time.sleep(3)
        genres.sync_genres_changes()
        time.sleep(2)

if __name__ == '__main__':

    # Блок для быстрого чтения и удаления индексов - чтобы проверить что все работает
    # persons = PGtoESPersons()
    # films = PGtoESFilms()
    # genres = PGtoESGenres()
    """1. быстрое удаление индекса для проверки - потом удалить для персон """
    # index_name = 'persons_test'
    # print(f' eto personsle.read_index(index_name) : {persons.read_index(index_name)}')
    # print(f' eto persons.del_index(index_name) : {persons.del_index(index_name)}')

    """2 быстрое удаление индекса для проверки - потом удалить для фильмов """
    # index_name = 'films_test'
    # print(f' eto films.read_index(index_name) : {films.read_index(index_name)}')
    # print(f' eto films.del_index(index_name) : {films.del_index(index_name)}')

    """3 быстрое удаление индекса для проверки - потом удалить для жанров """
    # index_name = 'genres_test'
    # print(f' eto genres.read_index(index_name) : {genres.read_index(index_name)}')
    # print(f' eto genres.del_index(index_name) : {genres.del_index(index_name)}')
    do_etl()


