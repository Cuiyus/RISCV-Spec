from time import time

def handle(username):
    user_id = -1

    start = time()

    try:
        user_id = int(username.split("_")[-1])
    except Error as e:
        user_id = -1

    latency = time() - start
    #print(latency)
    return str(user_id)

