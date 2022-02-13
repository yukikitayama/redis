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
def get_articles(conn: redis.Redis, page, order='score:'):
    # Convert it to 0-based index
    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1

    # Get keys from ZSET by value order by reverse order
    # because we want articles from the highest score
    ids = conn.zrevrange(order, start, end)
    articles = []
    for id in ids:
        print(f'id: {id}')

        # HGETALL returns list of fields and values as dictionary at the key
        article_data = conn.hgetall(id)
        print(f'article_data: {article_data}')
        # As python data to identify, add the id as well to each data
        article_data['id'] = id
        articles.append(article_data)

    return articles


def add_remove_groups(conn: redis.Redis, article_id, to_add=[], to_remove=[]):
    article = 'article:' + article_id
    for group in to_add:
        conn.sadd('group:' + group, article)
    for group in to_remove:
        conn.srem('group:' + group, article)


def get_group_articles(conn: redis.Redis, group, page, order='score:'):
    key = order + group
    if not conn.exists(key):

        # e.g. key: 'score:new-group', ['group:new-group', 'score:']
        # 'group:new-group' is SET, 'score:' is ZSET, 'score:new-group' is ZSET
        # Here intersection of SET and ZSET, so output score just from ZSET
        # If both are ZSET, aggregate logic is applied
        conn.zinterstore(
            key,
            ['group:' + group, order],
            aggregate='max'
        )
        # Expire in 60 seconds
        conn.expire(key, 60)

    return get_articles(conn, page, key)


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

    article_id = '1'

    # Print HASH
    # r = conn.hgetall('article:' + article_id)
    # pprint.pprint(r)
    # print()

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
    articles = get_articles(conn, page=1)
    pprint.pprint(articles)
    print()

    # Add the current article to a new group
    # add_remove_groups(conn, article_id, to_add=['new-group'])
    # print('We added the article to a new group, other articles include:')

    # Get group
    articles = get_group_articles(conn, group='new-group', page=1)
    print('Get articles by group')
    pprint.pprint(articles)
    print()

    # If need, delete all the keys in redis
    # keys(PATTERN) returns a list of all keys matching pattern
    # So to_del is a concatenated list
    to_del = (
        conn.keys('time:*')
        + conn.keys('voted:*')
        + conn.keys('score:*')
        + conn.keys('article:*')
        + conn.keys('group:*')
    )
    print(f'to_del: {to_del}')
    # if to_del:
    #     conn.delete(*to_del)


if __name__ == '__main__':
    main()
