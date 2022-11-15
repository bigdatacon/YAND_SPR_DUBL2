import time
from pg_to_es_twoo import PGtoES

example = PGtoES()

"""быстрое удаление индекса для проверки - потом удалить """
# index_name = 'persons_test'
# print(f' eto example.del_index(index_name) : {example.del_index(index_name)}')
while True:
    example.sync_persons_changes()
    time.sleep(3)