import logging
from datetime import datetime
from typing import List, Set

from pg_loader_two import PGLoader
from es_saver_two import ESSaver
from state_two import State, JsonFileStorage

logger = logging.getLogger(__name__)


class PGtoES(PGLoader, ESSaver):
    def __init__(self, batch_size: int = 100):
        self.state = State(JsonFileStorage())
        self.batch_size = batch_size

    def __get_last_updated(self, index):
        last_updated_time = self.state.get_state(index + '_last_update')
        return last_updated_time if last_updated_time else datetime.min

    def find_person_id_after_update(self, last_updated):
        sql_1_p_change = f"SELECT id, updated_at FROM content.person WHERE updated_at > '{self.__get_last_updated('persons2')}' ORDER BY updated_at"
        res = self.do_query(sql_1_p_change)
        person_ids_where_person_changed = set(i.get('id') for  i in res)
        return person_ids_where_person_changed

    def find_film_change_where_person_changed(self, person_ids_where_person_changed):
        sql_2_film_change_where_person_changed = """SELECT fw.id, fw.updated_at \
                                                FROM content.film_workmovie fw \
                                                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id WHERE pfw.person_id IN ('{}') ORDER BY fw.updated_at""".format("','".join(person_ids_where_person_changed))

        res_2 = self.do_query(sql_2_film_change_where_person_changed)
        film_ids_where_person_changed = set(i.get('id') for i in res_2)
        return film_ids_where_person_changed

    def find_all_film_data_where_person_changed(self, film_ids_where_person_changed):
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
        res_3 = self.do_query(sql_3_all_film_data_where_person_changed)
        return res_3