import json
from pg_to_es_two.logger_settings.logger_settings import logger

class Schemes:
    def __init__(self):
        self.__scheme = None
    def get_schemes(self):
        try:
            if not self.__scheme:
                with open('schemes.json') as json_file:
                    self.__scheme = json.load(json_file)
        except Exception as e:
            logger.warning(f'except in get_schemes : {e.args}')
        return self.__scheme

