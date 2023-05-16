import redis

r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()
# p.subscribe('my_channel')#for testing socket
p.subscribe('1')


for message in p.listen():
    if message['type'] == 'message':
        print(message['data'].decode())
