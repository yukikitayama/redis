import redis


HOST = ''
PORT = ''
PASSWORD = ''


r = redis.Redis()
r.set('hello', 'world')
print(r.get('hello'))
