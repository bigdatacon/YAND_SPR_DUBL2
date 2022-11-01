# YAND_SPR_DUBL2
Повтор первого спринта чтобы отследить баги на новых названиях моделей 

#первичная инициализация базы 
docker exec -it postgres_movies2 bash где postgres_movies2 - имя контейнера с постгре
-далее выполнить команды из create_shema_and_tables.sql

#running
docker-compose build
docker-compose up

проверить работу api через файл api_test

