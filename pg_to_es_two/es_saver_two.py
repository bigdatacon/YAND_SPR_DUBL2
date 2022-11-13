import logging
import requests
from elasticsearch import Elasticsearch, helpers
from typing import List
logger = logging.getLogger(__name__)

#teory https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py
#teory good https://github.com/elastic/elasticsearch-py/issues/1698

# from settings.settings import Settings
# from settings.schemes import Schemes
from settings_two import Settings
from schemes import Schemes
from resources_two import backoff
from elasticsearch import  Elasticsearch



#!/usr/bin/env python
# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

"""Script that downloads a public dataset and streams it to an Elasticsearch cluster"""

import csv
from os.path import abspath, join, dirname, exists
import tqdm
import urllib3
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk


NYC_RESTAURANTS = (
    "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD"
)
DATASET_PATH = join(dirname(abspath(__file__)), "nyc-restaurants.csv")
CHUNK_SIZE = 16384



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

    def create_index2(self, index_name):

        self.__get_es_client().indices.create(index=index_name, body=load_json(config_fname))



    def create_index(self, client):
        """Creates an index in Elasticsearch if one isn't already there."""
        client.indices.create(
            index="nyc-restaurants",
            body={
                "settings": {"number_of_shards": 1},
                "mappings": {
                    "properties": {
                        "name": {"type": "text"},
                        "borough": {"type": "keyword"},
                        "cuisine": {"type": "keyword"},
                        "grade": {"type": "keyword"},
                        "location": {"type": "geo_point"},
                    }
                },
            },
            ignore=400,
        )


    def generate_actions(self):
        """Reads the file through csv.DictReader() and for each row
        yields a single document. This function is passed into the bulk()
        helper to create many documents in sequence.
        """
        with open(DATASET_PATH, mode="r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                doc = {
                    "_id": row["CAMIS"],
                    "name": row["DBA"],
                    "borough": row["BORO"],
                    "cuisine": row["CUISINE DESCRIPTION"],
                    "grade": row["GRADE"] or None,
                }

                lat = row["Latitude"]
                lon = row["Longitude"]
                if lat not in ("", "0") and lon not in ("", "0"):
                    doc["location"] = {"lat": float(lat), "lon": float(lon)}
                yield doc


    def main(self):
        print("Loading dataset...")
        number_of_docs = download_dataset()

        client = Elasticsearch('http://127.0.0.1:9200'
            # Add your cluster configuration here!
        )
        print("Creating an index...")
        create_index(client)

        print("Indexing documents...")
        progress = tqdm.tqdm(unit="docs", total=number_of_docs)
        successes = 0
        for ok, action in streaming_bulk(
            client=client, index="nyc-restaurants", actions=generate_actions(),
        ):
            progress.update(1)
            successes += ok
        print("Indexed %d/%d documents" % (successes, number_of_docs))





if __name__ == "__main__":
    # es_link = "http://127.0.0.1:9200"
    index = 'nyc-restaurants'
    client = Elasticsearch('http://127.0.0.1:9200'
                           # Add your cluster configuration here!
                           )
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
    print(example.get_schemes())


