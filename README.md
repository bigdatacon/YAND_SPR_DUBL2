# YAND_SPR_DUBL2
Повтор первого спринта чтобы отследить баги на новых названиях моделей. Также добавлен эластик  

running:

docker-compose build

docker-compose up

далее 1 РАЗ в контейнере postgres(тут название контейнера ) - в него нужно провалиться и выполнить скрипты из файла create_shema_and_tables.sql
далее 1 раз выполнить файл sqlite_to_postgres.py

#первичная инициализация базы 

docker exec -it postgres_movies2 bash где postgres_movies2 - имя контейнера с постгре
-далее выполнить команды из create_shema_and_tables.sql



#running

docker-compose build

docker-compose up

проверить работу api через файл api_test

Если джанго запускать вне докера, то поменять местами закомментированную часть в settings в databases и установить отдельно requirements txt и далее запустить джанго через manage.py runserver 8080


I. Информация по ETL

ETL в 2 вариациях (вариация etl работает стабильнее чем etl_two), обе работают, в docker-compose.yml чтобы запустить 1 вариацию нужно раскоментировать блок etl и закоментировать etl_two, сейчас наоборот.
Чтобы запустить файл etl в папке pg_to_es_two вне докера, нужно в settings поставить такие настройки 

{
  "film_work_pg": {
    "host": "127.0.0.1",
    "port": 5433,
    "dbname": "movies",
    "password": "postgres",
    "user": "postgres"
  },
  "film_work_es": {
    "host": "127.0.0.1",
    "port": 9200
  }
}

-- для быстрой проверки работы создания/удаления/чтение индексов раскомментировать строки в файле pg_to_es_two.etl которые идут после if __name__==__main - до последней строки etl(). Ее(последнюю строку etl()) - наоборот закомментировать. 
Так можно бытсро проверить что все работает
Также работу можно проверить через ipython
import requests
#вывести все индексы 
 ans = requests.get("http://127.0.0.1:9200/_aliases")
 ans.json()

#прочитать индекс (он же таблица в эластик):
index_name = 'genres_test'
ans = requests.get("http://127.0.0.1:9200/genres_test/_search")
ans.json()





II. Дополнительная информация 

#на некоторых системах в датаклассах в (и Person_film_wor)
@dataclass
class Genre_film_work:

Поля  

    film_work_id:         str
    genre_id:   str
    film_work_id:         str
    person_id:   str
    
    
    Нужно заменить на 
    
    
    film_work:         str
    genre:   str
    film_work:         str
    person:   str


III.
Важная теория по эластику
#teory https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py

#teory good https://github.com/elastic/elasticsearch-py/issues/1698

#bulk : https://towardsdatascience.com/how-to-index-elasticsearch-documents-with-the-bulk-api-in-python-b5bb01ed3824

# https://sunscrapers.com/blog/elasticsearch-python-7-tips-best-practices/


