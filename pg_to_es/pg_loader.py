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
    print(example._PGLoader__get_cursor())
    # print(example.do_query(sql_string))
    for i in example.do_query(sql_string):
        # print(f' eto i : {i}')
        for k,v in i.items():
            print({k: v})


