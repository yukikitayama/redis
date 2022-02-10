# redis

- Stands for `REmote DIctionary Server`.
- Understand concept and learn how to use it
- [DB-Engines Ranking](https://db-engines.com/en/ranking)

## Todo

- [ ] [1.3.1 Voting on articles](https://redis.com/ebook/part-1-getting-started/chapter-1-getting-to-know-redis/1-3-hello-redis/1-3-1-voting-on-articles/)

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

## Python

- Redis is Python friendly.
- `pip install redis`
- [Redis with Python](https://docs.redis.com/latest/rs/references/client_references/client_python/)
- [How to Use Redis With Python](https://realpython.com/python-redis/#using-redis-py-redis-in-python)
- `zadd(KEY, PYTHON_DICTIONARY)`
  - [not able to insert data using ZADD(sorted set ) in redis using python](https://stackoverflow.com/questions/53553009/not-able-to-insert-data-using-zaddsorted-set-in-redis-using-python)

## GitHub

- [Redis in Action](https://github.com/josiahcarlson/redis-in-action)

## Book

- [Redis in Action](https://redis.com/ebook/redis-in-action/)

## Sharding

- A method to partition data into different pieces.
- Data is partitioned by IDs embedded in key
- It allows us to store and fetch data from multiple machines in a better performance.