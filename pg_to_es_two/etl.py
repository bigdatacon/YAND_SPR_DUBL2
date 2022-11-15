import time
from pg_to_es_persons import PGtoESPersons

example = PGtoESPersons()

"""быстрое удаление индекса для проверки - потом удалить """
# index_name = 'persons_test'
# print(f' eto example.del_index(index_name) : {example.del_index(index_name)}')
# print(f' eto example.read_index(index_name) : {example.read_index(index_name)}')
while True:
    example.sync_persons_changes()
    time.sleep(3)