import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0)
initiated=False

while True:
    if not initiated:
        print("publisher initiated")
        initiated=True
    message = f"Hello world! {time.time()}"
    r.publish('my_channel', message)
    time.sleep(0.2)
