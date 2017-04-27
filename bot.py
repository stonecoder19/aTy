from time import sleep

import updates
from setup import setup_apis
from exceptions import UpdateError

apis = setup_apis()

next_update = updates.get_next_update(apis)
last_updated_time = next_update.time

while True:
    try:
        next_update.update()

        next_update = updates.get_next_update(apis, last_updated_time)
        sleep(updates.INTERVAL)

    except UpdateError as e:
        print(e)
        next_update = updates.get_next_update(apis, last_updated_time)
