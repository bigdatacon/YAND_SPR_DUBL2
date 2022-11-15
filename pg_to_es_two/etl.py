import time
from pg_to_es_twoo import PGtoES

example = PGtoES()
while True:
    example.sync_persons_changes()
    time.sleep(3)