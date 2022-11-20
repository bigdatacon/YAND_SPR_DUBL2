import json
from logger_settings.logger_settings import logger

class Schemes:
    def __init__(self):
        self.__scheme = None
    def get_schemes(self):
        try:
            if not self.__scheme:
                with open('schemes_predv.json') as json_file:
                    self.__scheme = json.load(json_file)
        except Exception as e:
            logger.warning(f'except in get_schemes : {e.args}')
        return self.__scheme

