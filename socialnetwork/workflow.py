import threading
from time import time
import json
import random
from concurrent.futures import ThreadPoolExecutor, wait

from function.compose_post import handle as compose_post_handle
from function.upload_media import handle as upload_media_handle
from function.upload_unique_id import handle as upload_unique_id_handle
from function.upload_urls import handle as upload_urls_handle
from function.upload_text import handle as upload_text_handle
from function.upload_user_mentions import handle as upload_user_mentions_handle
from function.upload_creator import handle as upload_creator_handle
from function.compose_and_upload import handle as compose_and_upload_handle

threadPool = ThreadPoolExecutor(max_workers=8)


def send_post(handler, req):
    r = handler(req)

def upload_text_send_post(req):
    upload_text_res = upload_text_handle(req)
    upload_text_res_j = json.loads(upload_text_res)

    ut_t = []
    ut_futures = []
    utt1_future = threadPool.submit(send_post, upload_urls_handle, upload_text_res)
    utt2_future = threadPool.submit(send_post, upload_user_mentions_handle, upload_text_res)
    ut_futures.append(utt1_future)
    ut_futures.append(utt2_future)
    wait(ut_futures)

def sn_flow(req):
    start = time()

    req = compose_post_handle(req)
    req_j = json.loads(req)
    req_id = str(req_j["req_id"])
    
    compose_futures = []
    upload_text_future = threadPool.submit(upload_text_send_post, req)
    compose_futures.append(upload_text_future)
    for temp_handle in [upload_unique_id_handle, upload_media_handle, upload_creator_handle]:
        future = threadPool.submit(send_post, temp_handle, req)
        compose_futures.append(future)
    wait(compose_futures)
    

    upload_res = compose_and_upload_handle(req_id)
   
    print(upload_res)
    return str(time() - start)

def handle(req_id):
    """handle a request to the function
    Args:
        req (str): request body
    """
    u1 = random.randint(1, 1000)
    u2 = (u1+1) % 1000
    req = '{"req_id": '+str(req_id)+', "media_ids":"dog777.png,dog7777.png", "media_types":"png,png","media_urls":"http://192.168.1.109/file/dog.jpg,http://192.168.1.109/file/dog.jpg", "user_id": '+str(u1)+', "username":"username_'+str(u1)+'","text":"hello @username_'+str(u2)+', we like http://baidu.com and http://google.com http://baidu.com/s/search http://baidu.com/s/search&dog.jpg baidu.com/s/search&dog.jpg", "post_type": 0}'

    return sn_flow(req)
