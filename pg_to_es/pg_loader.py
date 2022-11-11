import psycopg2
import psycopg2.extras
from psycopg2 import DatabaseError

from settings import Settings
from resources import backoff


class PGLoader(Settings):

    __pg_con = None
    __cursor = None

    def do_query(self, sql: str):
        try:
            self.__get_cursor().execute(sql)
            return self.__cursor.fetchall()
        except DatabaseError:
            self.__pg_con.close()
            self.__cursor = None

    # @backoff()
    def __get_cursor(self):
        if not self.__cursor:
            self.__pg_con = psycopg2.connect(**self.__get_db_params())
            self.__cursor = self.__pg_con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return self.__cursor

    def __get_db_params(self):
        return dict(self.get_settings().film_work_pg)

if __name__ == '__main__':
    example =PGLoader()
    print(example._PGLoader__get_db_params())
    sql_string = 'select * from content.genre;'
    # sql_string_long = """
    #         SELECT DISTINCT
    #             gfw.film_work_id AS film_work_id,
    #             pfw.person_id AS person_id,
    #             g.id AS genre_id,
    #             g.updated_at
    #         FROM content.genre g
    #         LEFT JOIN content.genre_film_work gfw ON g.id = gfw.genre_id
    #         LEFT JOIN content.film_workmovie fw ON gfw.film_work_id = fw.id
    #         LEFT JOIN content.person_film_work pfw ON fw.id = pfw.film_work_id """

    # sql_string_long = """
    #         SELECT
    #             p.id,
    #             p.full_name,
    #             ARRAY_AGG(DISTINCT jsonb_build_object('id', fw.id, 'role', pfw.role, 'title', fw.title)) AS films
    #
    #         FROM content.person p
    #         LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
    #         LEFT JOIN content.film_workmovie fw ON pfw.film_work_id = fw.id
    #         GROUP BY p.id
    #         """

    # sql_string_long = """            SELECT
    #             fw.id,
    #             fw.rating as imdb_rating,
    #             STRING_AGG(DISTINCT g.name, ' ') as genre,
    #             ARRAY_AGG(DISTINCT jsonb_build_object('id', g.id, 'name', g.name)) AS genres,
    #             fw.title,
    #             fw.description,
    #             ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director') AS director,
    #             ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
    #             ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names,
    #             ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'actor') AS actors,
    #             ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) FILTER (WHERE pfw.role = 'writer') AS writers
    #         FROM content.film_workmovie fw
    #         LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    #         LEFT JOIN content.genre g ON g.id = gfw.genre_id
    #         LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    #         LEFT JOIN content.person p ON p.id = pfw.person_id
    #         GROUP BY fw.id"""
    sql_string_long = """            SELECT
                ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director') AS director,
                ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor') AS actors_names,
                ARRAY_AGG(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer') AS writers_names

            FROM content.film_workmovie fw
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            GROUP BY fw.id"""
    # sql_string_long = """
    #         SELECT
    #             # p.id,
    #             # p.full_name,
    #             ARRAY_AGG(DISTINCT jsonb_build_object('id', fw.id, 'role', pfw.role, 'title', fw.title)) AS films
    #         FROM content.person p
    #         LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
    #         LEFT JOIN content.film_workmovie fw ON pfw.film_work_id = fw.id
    #
    #         GROUP BY p.id
    #
    #         """

    # sql_string_long = """SELECT *
    #             from  content.film_workmovie fwm join content.genre_film_work gfw on fwm.id = gfw.film_work_id"""

    # print(example._PGLoader__get_cursor())
    print(example.do_query(sql_string_long))
    # records = example.do_query(sql_string_long)

    # update_at = [r['updated_at'].strftime('%Y-%m-%d %H:%M:%S.%f') for r in records][:3] if records else None
    # print(f' this records : {records[:3]}')
    # print(f' this update_at : {update_at}')
    # for i in example.do_query(sql_string_long):
    #     # print(f' eto i : {i}')
    #     for k,v in i.items():
    #         print({k: v})


