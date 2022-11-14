import psycopg2
import psycopg2.extras
from psycopg2 import DatabaseError
from psycopg2 import Error
from settings_two import Settings
from datetime import datetime

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
    last_state = datetime.min
    print(last_state)
    # res = example.do_query("""select * from content.genre where updated_at>'{}'""".format(last_state))
    res = example.do_query(f"select * from content.genre where updated_at>'{last_state}'")
    print(res)
    for i in res:

        print(i.get('updated_at'), i.get('updated_at').strftime("%Y-%m-%d %H:%M:%S.%f"), i.get('updated_at').strftime("%Y-%m-%d %H:%M"))
        break

    """За всеми обновлёнными именами людей за промежуток времени. Запрос получается очень простым:"""

    sql_1_p_change = f"SELECT id, updated_at FROM content.person WHERE updated_at > '{last_state}' ORDER BY updated_at"
    sql_2_film_change_where_person_changed = f"""SELECT fw.id, fw.updated_at
                                                FROM content.film_work fw
                                                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                                                WHERE pfw.person_id IN (<id_всех_людей>)
                                                ORDER BY fw.updated_at"""




