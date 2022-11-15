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
    # res = example.do_query(f"select * from content.genre where updated_at>'{last_state}'")
    # print(res)
    # for i in res:
    #
    #     print(i.get('updated_at'), i.get('updated_at').strftime("%Y-%m-%d %H:%M:%S.%f"), i.get('updated_at').strftime("%Y-%m-%d %H:%M"))
    #     break

    """За всеми обновлёнными именами людей за промежуток времени. Запрос получается очень простым:"""

    sql_1_p_change = f"SELECT id, updated_at FROM content.person WHERE updated_at > '{last_state}' ORDER BY updated_at"
    res = example.do_query(sql_1_p_change)
    person_ids_where_person_changed = set(i.get('id') for  i in res)
    # print(person_ids_where_person_changed)


    # sql_2_film_change_where_person_changed = f"SELECT fw.id, fw.updated_at \
    #                                             FROM content.film_workmovie fw \
    #                                             LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id \
    #                                             # WHERE pfw.person_id IN (79b1c0ba-71f8-4fb2-b22c-ae417d898d78) \
    #                                             # ORDER BY fw.updated_at"

    sql_2_film_change_where_person_changed = "SELECT fw.id, fw.updated_at \
                                                FROM content.film_workmovie fw \
                                                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id WHERE pfw.person_id IN ('{}') ORDER BY fw.updated_at".format("','".join(person_ids_where_person_changed))

    res_2 = example.do_query(sql_2_film_change_where_person_changed)
    film_ids_where_person_changed = set(i.get('id') for i in res_2)
    # film_ids_where_person_changed = " , ".join(film_ids_where_person_changed)
    # print(film_ids_where_person_changed)

    sql_3_all_film_data_where_person_changed = """SELECT
                                                fw.id as fw_id,
                                                fw.title,
                                                fw.description,
                                                fw.rating,
                                                fw.type,
                                                fw.created_at,
                                                fw.updated_at,
                                                pfw.role,
                                                p.id,
                                                p.full_name,
                                                g.name
                                            FROM content.film_workmovie fw
                                            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                                            LEFT JOIN content.person p ON p.id = pfw.person_id
                                            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                                            LEFT JOIN content.genre g ON g.id = gfw.genre_id
                                            WHERE fw.id IN ('{}')""".format("','".join(film_ids_where_person_changed))



    res_3 = example.do_query(sql_3_all_film_data_where_person_changed)
    # print(res_3)

    print(example.do_query("select  ARRAY_AGG(DISTINCT jsonb_build_object('id', g.id, 'name', g.name)) AS genres_long from content.genre g" ))

