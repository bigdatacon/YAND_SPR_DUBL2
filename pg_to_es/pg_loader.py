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

    sql_string_long = """SELECT * 
            from  content.film_workmovie fwm  join content.genre_film_work gfw ON fwm.genres = gfw.genre"""
    print(example._PGLoader__get_cursor())
    print(example.do_query(sql_string_long))
    # for i in example.do_query(sql_string_long):
    #     # print(f' eto i : {i}')
    #     for k,v in i.items():
    #         print({k: v})


