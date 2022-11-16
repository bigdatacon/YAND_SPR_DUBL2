import logging
import requests
from typing import Optional
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
logger = logging.getLogger(__name__)
from resources_two import backoff


#teory https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py
#teory good https://github.com/elastic/elasticsearch-py/issues/1698


from settings_two import Settings
from schemes import Schemes
from elasticsearch import Elasticsearch






class ESSaver(Settings, Schemes):

    def __get_es_link(self):
        return f'http://{self.get_settings().film_work_es.host}:{self.get_settings().film_work_es.port}'

    def __get_es_client(self):
        return Elasticsearch(self.__get_es_link())

    def __delete_index(self, index_name):
        resp = requests.delete("{}/{}".format(self.__get_es_link(), index_name))
        if resp.status_code != 200:
            logger.warning(f"Ошибка создания поискового индекса: {resp.status_code, index_name}")
        else:
            logger.warning(f"DELETE индекс: {resp.status_code, index_name}")

    def __search_index(self, index_name):
        return Elasticsearch(self.__get_es_link()).search(index=index_name)

    @backoff()
    def create_index(self, index_name: str, scheme: Optional[dict]=None):
        scheme_it = scheme if scheme else  self.get_schemes().get(index_name)
        resp = requests.put("{}/{}".format(self.__get_es_link(), index_name), json=scheme_it)
        if resp.status_code != 200:
            logger.warning(f"Ошибка создания поискового индекса: {index_name}")
        else:
            print(f'создан индекс : {index_name}')
        # return self.__get_es_client().indices.create(index=index_name, **scheme_it)

    def save_one(self, index_name, doc):
        return self.__get_es_client().bulk(index_name, doc)

    @backoff()
    def save_many(self, index_name, docs):
        helpers.bulk(self.__get_es_client(), [{ "_id": el.get('id'), **el}
        for el in docs],
        index=index_name)






if __name__ == "__main__":
    # es_link = "http://127.0.0.1:9200"
    index = 'nyc-restaurants'
    index_real = 'genres2'
    test_index = 'test'
    client = Elasticsearch('http://127.0.0.1:9200')
    test_schemes = {
    "mappings": {
        "properties": {
            "text_field": {"type": "keyword"},
            "number": {"type": "long"}
        }
    }
    }
    test_data = {
    "text_field": "my pretty text test",
    "number": 111
    }
    test_docs = [
        {
            "text_field": "my pretty text test2",
            "number": 22
        },
        {
            "text_field": "my pretty text test3",
            "number": 33
        }
    ]

    # es = Elasticsearch(es_link)
    # print(es)
    # resp = requests.delete("{}/{}".format(es_link, index))
    # if resp.status_code != 200:
    #     logger.warning(f"Ошибка создания поискового индекса: {resp.status_code, index}")
    # else:
    #     logger.warning(f"DELETE индекс: {resp.status_code, index}")
    example = ESSaver()
    # print(example._ESSaver__get_es_link())
    # print(example.create_index(client))
    # print(example._ESSaver__delete_index(index))
    # print(example.get_schemes().get(index_real))
    # print(example.create_index2(index_real))
    # print(example._ESSaver__search_index(index_real))
    # print(example._ESSaver__delete_index(index))

    # print(example.create_index2(index, test_schemes))
    # print(example._ESSaver__search_index(index))
    #
    # print(example.save_one(index, test_data))
    # print(example._ESSaver__search_index(index))
    # print(example._ESSaver__delete_index(index))

    # print(client.index(index=index, document= test_data))
    # print(client.search(index='test'))
    # print(client.delete(index='test'))
    # print([el for el in actions_list])
    # helpers.bulk(client, [{"_index": 'index',  **el} for el in test_docs])
    # helpers.bulk(client, [el for el in test_docs],
    #      index=index)

    # print(example._ESSaver__delete_index(index))
    # helpers.bulk(client, [{ "_id": 1, **el}
    # for el in test_docs],
    # index=index)


    # print(example._ESSaver__search_index(index))


    #тестирование сохранения многих
    # print(example._ESSaver__delete_index(index))
    # print(example.create_index(index, test_schemes))
    # print(example._ESSaver__search_index(index))
    import random
    # helpers.bulk(example._ESSaver__get_es_client(), [{ "_id": random.randint(0, 100), **el}
    # for el in test_docs],
    # index=index)
    print(example._ESSaver__search_index(index))
    print(f'here datetime.min : {datetime.min}')
    print(f'here datetime.min : {datetime.min.strftime("%Y-%m-%d %H:%M:%S.%f")}')

