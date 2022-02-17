# redis

- Stands for `REmote DIctionary Server`.
- Understand concept and learn how to use it
- [DB-Engines Ranking](https://db-engines.com/en/ranking)
- Redis is another tool that we can use to solve problems.
- Redis offers
  - in-memory data making it fast
  - remote making it accessible to multiple clients and servers
  - persistent and scalable
- With Redis, our way of thinking will change from "How should I modify my data to fit into database tables and rows" to
  "Which structures in Redis will result in an easier-to-maintain solution?"
- Redis doesn't allow nested structures, which non-relational database user might expect.
  - Because Redis wants to keep the Redis command syntax simple.
  - To mitigate, find out a better key and save the additional information.

## Todo

- [ ] [3.7.2 Basic Redis transactions](https://redis.com/ebook/part-2-core-concepts/chapter-3-commands-in-redis/3-7-other-commands/3-7-2-basic-redis-transactions/)

## Basic

- Generally, choose to store data in Redis only when the performance or functionality of Redis is necessary.
  - Use other relational or non-relational database when slower performance is acceptable, or when too big for memory
- We will make keys in Redis that map to any one of the below 5 data structure types
  - `STRING`
  - `LIST`
    - Ordered sequence of strings
  - `SET`
    - Using a hash table to keep all strings unique in a set.
    - Unordered
    - No push and pop, but add and remove by value
  - `HASH`
    - Mapping of keys to values
    - Gets translated into a dictionary in Python
    - Similar to a document in a document store, or a row in a relational database, in that we can access or change
      individual or multiple fields at a time.
  - `ZSET`
    - Sorted set
    - Keys are unique
    - Values are limited to floating-point numbers.

### String

- Confusing because `STRING` contains byte string, integer, and floating-point
- Integer range is signed 64-bit integers on 64-bit machine.
- In Redis, when setting a `STRING` value which can be interpreted as a base-10 integer or floating-point, Redis detects
  and allow us to manipulate by numeric operation such as increment.
- If we increment a key which doesn't exist, Redis behaves like the key's value was 0.
- Below we can set a number as a string, Redis detects it's a number and allow us to increment it, and even if it
  originally didn't exist.

```
>>> redis_client.set('KEY', '1')
True
>>> redis_client.incr('KEY')
2
```

### List

- Good to store a queue of work items, e.g. Recently viewed articles or favorite contacts.
- `conn.lrange('KEY', 0, -1)`
  - See all the items in `LIST`.
- `conn.rpush('KEY', 'a', 'b', 'c')`
  - Push multiple items one time from right

### Set

- Redis `SET` semantics, such as intersection or union, is very similar to Python set.
- But the benefit of Redis `SET` is that Redis `SET` is available remotely to many clients.

### Hash

- `conn.hincrby('KEY_NAME', 'KEY', INCREMENT)`
  - Increment the value stored at the given key in `HASH` by the integer increment
  - Incrementing a previously nonexistent key in `HASH` in Redis is okay, because Redis operates as though the value
    had been 0 and increment.

### Zset

- `conn.zrank('KEY_NAME', 'KEY')`
  - Fetch the 0-indexed position of a member.
  - e.g. `ZSET` ZSET contains 3 elements, and key a is the bottom, and `conn.zrank('ZSET', 'a')` returns 2.
- `ZINTERSTORE` is getting intersection of `ZSET`. By default, values are summed up.

```
>>> conn.zadd('zset-1', 'a', 1, 'b', 2, 'c', 3)
>>> conn.zadd('zset-2', 'b', 4, 'c', 1, 'd', 0)
>>> conn.zinterstore('zset-i', ['zset-1', 'zset-2'])
>>> conn.zrange('zset-i', 0, -1, withscores=True)
[('b', 6.0), ('c', 4.0)]
```

- `ZSET` can be unioned and intersectioned with `SET`
  - A member in `SET` behave as if they were `ZSET` with all scores equal to 1.

### Sorting

- You can sort numerically or alphabetically the number interpretable `STRING`.

```
>>> conn.rpush('sort-input', 23, 15, 110, 7)

# Sorting numerically
>>> conn.sort('sort-input')
['7', '15', '23', '110']

# Sorting alphabetically
>>> conn.sort('sort-input', alpha=True)
['110', '15', '23', '7']
```

## Atomic

- It means that no other client can read or change data while we are reading or changing the same data
  - Redis describes some commands as atomic.

## Redis Cloud

- [Connect to a database](https://docs.redis.com/latest/rc/rc-quickstart/)

## RedisJSON

- [RedisJSON Commands in Python](https://redis-py.readthedocs.io/en/stable/redismodules.html#redisjson-commands)

## Python

- Redis is Python friendly.
- `pip install redis`
- [redis-py documentation](https://redis-py.readthedocs.io/en/stable/)
- [Redis with Python](https://docs.redis.com/latest/rs/references/client_references/client_python/)
- [How to Use Redis With Python](https://realpython.com/python-redis/#using-redis-py-redis-in-python)
- `zadd(KEY, PYTHON_DICTIONARY)`
  - [not able to insert data using ZADD(sorted set ) in redis using python](https://stackoverflow.com/questions/53553009/not-able-to-insert-data-using-zaddsorted-set-in-redis-using-python)

## GitHub

- [Redis in Action](https://github.com/josiahcarlson/redis-in-action)

## Book

- [Redis in Action](https://redis.com/ebook/redis-in-action/)

## GUI

- [How Can I Browse/View The Values Stored in Redis [closed]](https://stackoverflow.com/questions/12292351/how-can-i-browse-view-the-values-stored-in-redis)
- [Redsmin - Redis GUI](https://www.redsmin.com/)

## Sharding

- A method to partition data into different pieces.
- Data is partitioned by IDs embedded in key
- It allows us to store and fetch data from multiple machines in a better performance.