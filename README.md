# YAND_SPR_DUBL2
Повтор первого спринта чтобы отследить баги на новых названиях моделей 

#первичная инициализация базы 
docker exec -it postgres_movies2 bash где postgres_movies2 - имя контейнера с постгре
-далее выполнить команды из create_shema_and_tables.sql

#running

docker-compose build

docker-compose up

проверить работу api через файл api_test

Если джанго запускать вне докера, то поменять местами закомментированную часть в settings в databases и установить отдельно requirements txt и далее запустить джанго через manage.py runserver 8080

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
