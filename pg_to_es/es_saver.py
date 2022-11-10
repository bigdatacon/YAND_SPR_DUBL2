import logging
import requests
from elasticsearch import Elasticsearch, helpers
from typing import List
logger = logging.getLogger(__name__)

# from settings.settings import Settings
# from settings.schemes import Schemes
from settings import Settings
from schemes import Schemes
from resources import backoff


class ESSaver(Settings, Schemes):

    __es_con = None

    SCHEMES = {
        "movies": 'film_scheme',
        "persons": 'person_scheme',
        "genres": 'genre_scheme',
    }

    test_schemes = {
    "mappings": {
        "properties": {
            "text_field": {"type": "keyword"},
            "number": {"type": "long"}
        }
    }
    }

    @backoff()
    def save_one(self, doc: dict, index: str):
        self.__get_connection().index(index=index, id=doc['id'], document=doc)

    def test_save_one(self, doc: dict, index: str):
        try:
            self.test_get_connection().index(index=index,  document=doc)
        except Exception as e:
            print(f' except in test_save_one : {e.args}')

    def test_read_index(self, index):
        ans = self.test_get_connection().search(index=index)
        return ans


    @backoff()
    def save_many(self, docs: List[dict], index: str):
        helpers.bulk(self.__get_connection(), [{'_index': index, '_id': doc['id'], **doc} for doc in docs])


    def test_get_connection(self):
        host_link = self.__get_es_link().replace('elastic', '127.0.0.1')
        if not self.__es_con:
            self.__es_con = Elasticsearch(host_link)
        return self.__es_con

    def __get_connection(self):
        if not self.__es_con:
            self.__es_con = Elasticsearch(self.__get_es_link())
        return self.__es_con

    def __get_es_link(self):
        es_params = dict(self.get_settings().film_work_es)
        return f"http://{es_params['host']}:{es_params['port']}"


    def test_get_scheme(self, index: str):
        scheme = self.get_schemes()[self.SCHEMES[index]]
        return scheme


    def test_delete_index(self, index: str):
        host_link = self.__get_es_link().replace('elastic', '127.0.0.1')
        resp = requests.delete("{}/{}".format(host_link, index))
        if resp.status_code != 200:
            logger.warning(f"Ошибка создания поискового индекса: {resp.status_code, index}")
        else:
            logger.warning(f"DELETE индекс: {resp.status_code, index}")

    @backoff()
    def test_create_index_127(self, index: str):
        scheme = self.get_schemes()[self.SCHEMES[index]]
        host_link = self.__get_es_link().replace('elastic', '127.0.0.1')
        logger.warning(f"this scheme: {scheme, host_link}")
        resp = requests.put("{}/{}".format(host_link, index), json=scheme)
        if resp.status_code != 200:
            logger.warning(f"Ошибка создания поискового индекса: {resp.status_code, index}")

        else:
            logger.warning(f"Create индекс: {resp.status_code, index}")

    def test_create_index_on_test_scheme(self, index: str):
        host_link = self.__get_es_link().replace('elastic', '127.0.0.1')
        logger.warning(f"this scheme: {self.test_schemes, host_link}")
        resp = requests.put("{}/{}".format(host_link, index), json=self.test_schemes)
        if resp.status_code != 200:
            logger.warning(f"Ошибка создания поискового индекса: {resp.status_code, index}")

        else:
            logger.warning(f"Create индекс: {resp.status_code, index}")



    @backoff()
    def create_index(self, index: str):
        scheme = self.get_schemes()[self.SCHEMES[index]]
        logger.debug(f"this scheme: {scheme}")
        resp = requests.put("{}/{}".format(self.__get_es_link(), index), json=scheme)
        if resp.status_code != 200:
            logger.warning(f"Ошибка создания поискового индекса: {index}")


if __name__ == '__main__':
    settings = Settings()
    # print(settings.get_settings())

    example =ESSaver()
    # print(example._ESSaver__get_es_link())
    # print(example.test_get_scheme('genres'))
    #1 create index
    index = 'genres'
    index_test = 'table4'
    test_data = {
    "text_field": "my pretty text test",
    "number": 111
    }
    # print(example.test_create_index_127(index))
    #2 delete index
    # print(example.test_delete_index(index))

    #3 create Elasticsearch connection
    # print(example.test_get_connection())

    #4 create test index(table)
    # print(example.test_create_index_on_test_scheme(index_test))

    #5 insert on record in index, created in point #4
    # print(example.test_save_one(test_data, index_test))

    #6 read index after insert data in point #
    print(example.test_read_index(index_test))




