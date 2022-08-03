from update_cars.bmw import update

import threading

def run():
    threading.Timer(3600.0, run).start() # called every minute
    update()

run()
