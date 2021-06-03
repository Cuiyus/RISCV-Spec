import redis

compose_post_redis = "127.0.0.1"

if __name__ == '__main__':
    cpr = redis.Redis(host=compose_post_redis, port=6379, decode_responses=True)
    for k in cpr.keys():
        cpr.delete(k)
