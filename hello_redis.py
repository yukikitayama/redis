import redis
import boto3
import json
import time
import pprint


# session = boto3.Session(profile_name='default')
SECRET_ID = 'redis'
REGION_NAME = 'us-west-1'
# 60 * 60 * 24 = 86400
ONE_WEEK_IN_SECONDS = 7 * 86400
VOTE_SCORE = 432
ARTICLES_PER_PAGE = 25


def get_secret(secret_id: str, region_name: str) -> dict:
    session = boto3.Session(profile_name='yuki')
    client = session.client(service_name='secretsmanager', region_name=region_name)
    content = client.get_secret_value(SecretId=secret_id)
    secret_string = content['SecretString']
    secret = json.loads(secret_string)
    return secret


def post_article(conn: redis.Redis, user, title, link):
    # incr() increments the value of key by amount, by default 1
    # If no key exists, the value will be initialized as amount
    article_id = str(conn.incr('article:'))

    voted = 'voted:' + article_id
    # Add voted:ARTICLE_ID to SET
    conn.sadd(voted, user)
    # Set an expire flag on key name for time seconds
    conn.expire(voted, ONE_WEEK_IN_SECONDS)

    # Creation datetime in Unit time
    now = time.time()
    article = 'article:' + article_id

    # Make HASH
    conn.hset(article, mapping={
        'title': title,
        'link': link,
        'poster': user,
        'time': now,
        'votes': 1
    })

    # Make ZSET if not exist and add
    conn.zadd('score:', {article: now + VOTE_SCORE})
    # Make ZSET if not exist and add
    conn.zadd('time:', {article: now})

    return article_id


def article_vote(conn: redis.Redis, user, article: str):
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    if conn.zscore('time:', article) < cutoff:
        return

    # Extract string ID from article string
    article_id = article.partition(':')[-1]
    # If the user hasn't voted before, True and add
    if conn.sadd('voted:' + article_id, user):
        conn.zincrby('score:', VOTE_SCORE, article)
        conn.hincrby(article, 'votes', 1)


# Get articles


def main():

    # Get secret
    secret = get_secret(secret_id=SECRET_ID, region_name=REGION_NAME)
    host = secret['host']
    port = secret['port']
    password = secret['password']

    # Connecting to Redis
    conn = redis.Redis(host=host, port=port, password=password, decode_responses=True)
    print(f'Ping: {conn.ping()}')
    print(f'Connection: {conn}')

    # Get all keys
    print(conn.keys('*'))

    # Upload one data to Redis
    # article_id = str(post_article(conn, 'Yuki', 'Title 1', 'http://www.google.com'))
    # print(f'Posted a new article with id: {article_id}')  # '1'
    # print()

    # Print HASH
    article_id = '1'
    r = conn.hgetall('article:' + article_id)
    pprint.pprint(r)
    print()

    # Print all in ZSET
    print(conn.zrange('time:', 0, -1, withscores=True))
    print(conn.zrange('score:', 0, -1, withscores=True))

    # Print all in SET
    print(conn.smembers('voted:1'))

    # Upvote
    # article_vote(conn, 'other_user', 'article:' + article_id)
    # print('We voted for the article, it now has votes:', end=' ')
    # # See values of a key in HASH
    v = int(conn.hget('article:' + article_id, 'votes'))
    print(v)
    print()

    # Get highest scoring article
    print('The currently highest-scoring articles are:')


if __name__ == '__main__':
    main()
