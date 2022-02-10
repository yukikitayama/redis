# redis

- Stands for `REmote DIctionary Server`.
- Understand concept and learn how to use it
- [DB-Engines Ranking](https://db-engines.com/en/ranking)

## Basic

- Generally, choose to store data in Redis only when the performance or functionality of Redis is necessary.
  - Use other relational or non-relational database when slower performance is acceptable, or when too big for memory
- We will make keys in Redis that map to any one of the below 5 data structure types
  - `STRING`
  - `LIST`
  - `SET`
  - `HASH`
  - `ZSET`
    - Sorted set. Ordered mapping of string members to floating-point scores, ordered by score.

## Redis Cloud

- [Connect to a database](https://docs.redis.com/latest/rc/rc-quickstart/)

## Todo

- [ ] [1.1.1 Redis compared to other databases and software](https://redis.com/ebook/part-1-getting-started/chapter-1-getting-to-know-redis/1-1-what-is-redis/1-1-1-redis-compared-to-other-databases-and-software/)

## Python

- Redis is Python friendly.
- `pip install redis`
- [Redis with Python](https://docs.redis.com/latest/rs/references/client_references/client_python/)

## GitHub

- [Redis in Action](https://github.com/josiahcarlson/redis-in-action)

## Book

- [Redis in Action](https://redis.com/ebook/redis-in-action/)

## Sharding

- A method to partition data into different pieces.
- Data is partitioned by IDs embedded in key
- It allows us to store and fetch data from multiple machines in a better performance.