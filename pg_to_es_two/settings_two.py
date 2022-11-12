from typing import Optional, List
from pydantic import BaseModel


class Film_work_pg(BaseModel):
    host: str
    port: int
    dbname: str
    password: str
    user: str


class Film_work_es(BaseModel):
    host: str
    port: int


class Config(BaseModel):
    film_work_pg: Film_work_pg
    film_work_es: Film_work_es
    def get_settings(self):
        return Config.parse_file('settings.json')



class Settings:
    def get_settings(self):
        return Config.parse_file('settings.json')


if __name__ == '__main__':
    #проверяю что работате парсинг в файле Config
    print(Config.parse_file('settings.json'))

    # #2 Проверяю что работате парсин файла в классе Config через функицю - не работает видимо так заложено в pydantic
    # config = Config()
    # print(config)
    # config = config.get_settings()
    # print(config)
    # #
    #3 Проверяю что работате парсин файла в основном классе
    config = Settings()
    config = config.get_settings()
    print(config)