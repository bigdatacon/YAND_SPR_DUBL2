# YAND_SPR_DUBL2
Повтор первого спринта чтобы отследить баги на новых названиях моделей 


running:
docker-compose build
docker-compose up

далее 1 РАЗ в контейнере postgres(тут название контейнера ) - в него нужно провалиться и выполнить скрипты из файла create_shema_and_tables.sql
далее 1 раз выполнить файл sqlite_to_postgres.py

Важная теория по эластику
#teory https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest/bulk-ingest.py
#teory good https://github.com/elastic/elasticsearch-py/issues/1698