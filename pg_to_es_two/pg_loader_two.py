import psycopg2
import psycopg2.extras
from psycopg2 import DatabaseError
from psycopg2 import Error
from settings_two import Settings

from settings_two import Settings
from resources_two import backoff

class PGLoader(Settings):
    __pg_con = None
    __pg_cursor = None

    def __get_db_params(self):
        return dict(Settings().get_settings().film_work_pg)

    def __get_cursor(self):
        self.__pg_con = psycopg2.connect(**self.__get_db_params())
        self.__pg_cursor = self.__pg_con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        return  self.__pg_cursor

    def do_query(self, sql: str):
        try:
            cursor = self.__get_cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except DatabaseError:
            self.__pg_con.close()
            self.__pg_cursor = None




if __name__ == '__main__':
    example = PGLoader()
    print(example._PGLoader__get_db_params())
    print(example._PGLoader__get_cursor())
    print(example.do_query('select * from content.genre'))

