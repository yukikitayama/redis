import redis


HOST = ''
PORT = ''
PASSWORD = ''


def main():

    # Redis client
    r = redis.Redis(host=HOST, port=PORT, password=PASSWORD)

    # String
    r.set('hello', 'world')
    print(r.get('hello'))

    # List
    r.rpush('list-key', 'item')
    r.rpush('list-key', 'item2')
    r.rpush('list-key', 'item')
    print(r.lrange('list-key', 0, -1))
    print(r.lindex('list-key', 1))

    # Set
    print(r.sadd('set-key', 'item'))
    print(r.sadd('set-key', 'item2'))
    print(r.sadd('set-key', 'item3'))
    print(r.sadd('set-key', 'item'))
    print('smembers', r.smembers('set-key'))
    print(r.sismember('set-key', 'item4'))
    print(r.sismember('set-key', 'item'))
    print('srem', r.srem('set-key', 'item2'))
    print('srem', r.srem('set-key', 'item2'))
    print('smembers', r.smembers('set-key'))

    # Hash
    print(r.hset('hash-key', 'sub-key1', 'value1'))
    print(r.hset('hash-key', 'sub-key2', 'value2'))
    print('already exist', r.hset('hash-key', 'sub-key1', 'value1'))
    # Hah gets translated into a dictionary in Python
    print(r.hgetall('hash-key'))
    print(r.hdel('hash-key', 'sub-key2'))
    print(r.hdel('hash-key', 'sub-key2'))
    print('get value', r.hget('hash-key', 'sub-key1'))

    # Zset
    print(r.zadd('zset-key', {'member1': 728}))
    print(r.zadd('zset-key', {'member0': 982}))
    print(r.zadd('zset-key', {'member0': 982}))
    print(r.zrange('zset-key', 0, -1, withscores=True))
    print(r.zrangebyscore('zset-key', 0, 800, withscores=True))
    print(r.zrem('zset-key', 'member1'))
    print(r.zrem('zset-key', 'member1'))
    print(r.zrange('zset-key', 0, -1, withscores=True))


if __name__ == '__main__':
    main()


