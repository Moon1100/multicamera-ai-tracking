# import redis

# r = redis.Redis(host='localhost', port=6379, db=0)
# p = r.pubsub()
# # p.subscribe('my_channel')#for testing socket
# p.subscribe('1')


# for message in p.listen():
#     if message['type'] == 'message':
#         print(message['data'].decode())


import redis

def listen_messages(channel):
    r = redis.Redis(host='192.168.0.105', port=6379, db=0)
    pubsub = r.pubsub()

    # Subscribe to the specified channel
    pubsub.subscribe(channel)

    print(f"Listening to channel: {channel}")

    # Start listening to messages
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received message: {message['data'].decode('utf-8')}")

if __name__ == '__main__':
    channel = '1'
    listen_messages(channel)
