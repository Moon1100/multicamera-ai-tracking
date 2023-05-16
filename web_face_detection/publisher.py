# import redis
# import time

# r = redis.Redis(host='localhost', port=6379, db=0)
# initiated=False

# while True:
#     if not initiated:
#         print("publisher initiated")
#         initiated=True
#     message = f"Hello world! {time.time()}"
#     r.publish('1', message)
#     time.sleep(0.2)



import redis
import time

def publish_message(channel):
    r = redis.Redis(host='192.168.0.108', port=6379, db=0)
    initiated = False

    while True:
        if not initiated:
            print("Publisher initiated")
            initiated = True

        message = f"Hello world! {time.time()}"
        r.publish(channel, message)
        time.sleep(0.2)

if __name__ == '__main__':
    channel = 'my_channel'
    publish_message(channel)
