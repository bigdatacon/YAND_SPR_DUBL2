import logging
from datetime import datetime
from typing import List, Set
import json
from typing import Optional
from pg_loader_two import PGLoader
from es_saver_two import ESSaver
from state_two import State, JsonFileStorage
from settings_two import Settings
from schemes import Schemes

logger = logging.getLogger(__name__)


class PGtoES(PGLoader, ESSaver):
    def __init__(self, batch_size: int = 100):
        self.state = State(JsonFileStorage())
        self.batch_size = batch_size
        self.schemes = Schemes()

    def __get_last_updated(self, index: Optional[str]=None):
        last_updated_time = self.state.get_state(index + '_last_update')
        return last_updated_time if last_updated_time else datetime.min

    def find_person_id_after_update(self):
        sql_1_p_change = f"SELECT id, updated_at FROM content.person WHERE updated_at > '{self.__get_last_updated('persons3')}' ORDER BY updated_at"
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

    def sync_to_elastic_index(self, index_name, res_3):
        if not self.state.get_state(index_name + '_last_update'):
            scheme = self.schemes.get_schemes().get(index_name)
            # print(f' here scheme{scheme}')
            self.create_index(index_name, scheme)
            print(f' index created')
            self.save_many(index_name, res_3)
        else:
            print(f' index yet created')
            self.save_many(index_name, res_3)


    def read_index(self, index_name):
        return self._ESSaver__search_index(index_name)

    def del_index(self, index_name):
        return self._ESSaver__delete_index(index_name)




if __name__ == '__main__':
    example = PGtoES()
    index_name = 'persons_test'
    # print(example._PGtoES__get_last_updated())
    last_state = example._PGtoES__get_last_updated(index_name)
    print(f'here last_state : {last_state}')
    #1проверка     print(example.find_person_id_after_update())
    person_ids_where_person_changed = example.find_person_id_after_update()
    # print(example.find_person_id_after_update())
    #2 проверка find_film_change_where_person_changed
    film_ids_where_person_changed = example.find_film_change_where_person_changed(person_ids_where_person_changed)
    # print(film_ids_where_person_changed)

    #3 проверка find_all_film_data_where_person_changed
    res_3 = example.find_all_film_data_where_person_changed(film_ids_where_person_changed)
    # print(res_3)

    with open('schemes_predv.json') as json_file:
        scheme = json.load(json_file)
    # print(f'here scheme : {scheme}')

    #4 проверка что работает создание индекса
    # print(example.test_schemes())
    # print(example.sync_to_elastic_index(index_name))

    #5 проверка что созданный индекс читается
    print(f' eto example.read_index(index_name) : {example.read_index(index_name)}')

    #6 проверка что индекс удаляется
    # print(f' eto example.del_index(index_name) : {example.del_index(index_name)}')


