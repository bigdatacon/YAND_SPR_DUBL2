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
import time

logger = logging.getLogger(__name__)


class PGtoESFilms(PGLoader, ESSaver):
    def __init__(self, batch_size: int = 100):
        self.state = State(JsonFileStorage())
        self.batch_size = batch_size
        self.schemes = Schemes()
        self.index_name = 'films_test'

    """1 Блок функций для заливки в эластик изменений по персонам"""

    def sync_films_changes(self):
        films_ids_where_person_changed = self.find_films_id_after_update()
        res_3 = self.find_all_film_data_where_person_changed(films_ids_where_person_changed)
        if res_3:
            self.sync_to_elastic_index(self.index_name, res_3)

    def find_films_id_after_update(self):
        sql_1_p_change = f"SELECT id, updated_at FROM content.film_workmovie WHERE updated_at > '{self.__get_last_updated(self.index_name + '_last_update')}' ORDER BY updated_at"
        res = self.do_query(sql_1_p_change)
        films_ids_where_person_changed = set(i.get('id') for i in res)
        return films_ids_where_person_changed

    def find_all_film_data_where_person_changed(self, film_ids_where_person_changed):
        sql_3_all_film_data_where_person_changed = """SELECT
                                                    fw.id as id,
                                                    fw.title,
                                                    fw.description,
                                                    fw.rating,
                                                    fw.type,
                                                    pfw.role,
                                                    p.full_name,
                                                    g.name as genre_name,
                                                    ARRAY_AGG(distinct jsonb_build_object('id', g.id, 'name', g.name)) AS genres_long

                                                FROM content.film_workmovie fw
                                                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                                                LEFT JOIN content.person p ON p.id = pfw.person_id
                                                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                                                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                                                WHERE fw.id IN ('{}')
                                                GROUP BY fw.id , pfw.id, p.id, g.id


                                                """.format("','".join(film_ids_where_person_changed))
        res_3 = self.do_query(sql_3_all_film_data_where_person_changed)
        return res_3

    """4. Блок вспомогательных функций"""

    def __get_last_updated(self, index: Optional[str] = None):
        last_updated_time = self.state.get_state(index + '_last_update')
        return last_updated_time if last_updated_time else datetime.min

    def sync_to_elastic_index(self, index_name, res_3):
        if not self.state.get_state(index_name + '_last_update'):
            scheme = self.schemes.get_schemes().get(index_name)
            # print(f' here scheme{scheme}')
            self.create_index(index_name, scheme)
            print(f' index {self.index_name} created')
            self.save_many(index_name, res_3)
            self.state.set_state(index_name + '_last_update', str(datetime.now()))
        else:
            print(f' index {self.index_name} yet created')
            self.save_many(index_name, res_3)
            self.state.set_state(index_name + '_last_update', str(datetime.now()))

    def read_index(self, index_name):
        return self._ESSaver__search_index(index_name)

    def del_index(self, index_name):
        return self._ESSaver__delete_index(index_name)


if __name__ == '__main__':
    example = PGtoESFilms()
    index_name = 'films_test'
    last_state = example._PGtoESFilms__get_last_updated(index_name)
    print(f'here last_state : {last_state}')

    # 1проверка     print(example.find_person_id_after_update())
    films_ids_where_person_changed = example.find_films_id_after_update()
    # print(f' here films_ids_where_person_changed : {films_ids_where_person_changed}')



    # 3 проверка find_all_film_data_where_person_changed
    res_3 = example.find_all_film_data_where_person_changed(films_ids_where_person_changed)
    # print(res_3)

    # with open('schemes_predv.json') as json_file:
    #     scheme = json.load(json_file)
    # print(f'here scheme : {scheme}')

    # 4 проверка что работает создание индекса и запись в него
    # print(example.test_schemes())
    # print(example.sync_to_elastic_index(index_name, res_3))

    # 5 проверка что созданный индекс читается
    # print(f' eto example.read_index(index_name) : {example.read_index(index_name)}')

    # 6 проверка что индекс удаляется
    # print(f' eto example.del_index(index_name) : {example.del_index(index_name)}')

    # 7 проверка что устанавливается состояние
    # print(str(datetime.now()))
    #
    # dict = {}
    # dict['test'] = str(datetime.now())
    # with open("state.json", 'w') as conf_file:
    #     state = json.dump(dict, conf_file)

    # 8 итоговая проверка что все работает для персон
    # while True:
    #     print(example.sync_persons_changes())
    #     time.sleep(3)




