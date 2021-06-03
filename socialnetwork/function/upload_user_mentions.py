import redis
import json
import time
from .get_user_id import handle as gui_handle

compose_post_redis = "127.0.0.1"

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    start = time.time()

    event = json.loads(req)

    req_id = str(event["req_id"])
    user_mentions = (event["user_mentions"]).split(",")

    user_mentions_str = ''
    for username in user_mentions:
        user_id = int(gui_handle(username))
        if user_id > 0:
            #user_mentions_str += '{"user_id": ' + str(user_id) + ', "username": "' + username + '"};'
            user_mentions_str += str(user_id) + ','
    user_mentions_str = user_mentions_str[:-1]

    r = redis.Redis(host=compose_post_redis, port=6379, decode_responses=True)
    r.hset(req_id, "user_mentions", user_mentions_str)
    #hlen_reply = r.hincrby(req_id, "num_components", 1)
    r.expire(req_id, 30)

    """
    if hlen_reply == 5:
        t = threading.Thread(target=send_post, args=(compose_and_upload_url, req_id))
        t.start()
    """
    return str(time.time() - start)

