import redis
import os

REDIS_HOST_SET = os.getenv('REDIS_HOST_SET').split(',')

def get_redis_connections(port=6379, db=0):
    return [redis.StrictRedis(host=redis_host.strip(), port=port, db=db) for redis_host in REDIS_HOST_SET]
