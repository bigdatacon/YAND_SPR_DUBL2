import logging
from datetime import datetime
from typing import List, Set

from pg_loader_two import PGLoader
from es_saver_two import ESSaver
from state_two import State, JsonFileStorage

logger = logging.getLogger(__name__)


class PGtoES(PGLoader, ESSaver):

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
    print(res_3)