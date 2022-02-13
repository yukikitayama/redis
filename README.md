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

## Todo

- [ ] [2.1 Login and cookie caching](https://redis.com/ebook/part-1-getting-started/chapter-2-anatomy-of-a-redis-web-application/2-1-login-and-cookie-caching/)

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