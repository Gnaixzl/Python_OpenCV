import cv2
import redis
import time
import sys
import os
import base64
# from turbojpeg import TurboJPEG
import turbojpeg
import multiprocessing
from multiprocessing.pool import ThreadPool, Pool


def get_data_from_redis(data_key, host, port, db):
    r = redis.StrictRedis(host=host, port=port, db=db)
    value = r.rpop(data_key)
    return value


def decode_base64(value, i):
    with open(f"out/redis_image_base64_{i}.jpg", "wb") as f:
        f.write(base64.b64decode(value))


def decode_types(value, i):
    with open(f'out/redis_image_types_{i}.jpg', 'wb') as f:
        f.write(value)


def decode_turbo(value, i):
    with open(f'out/redis_image_turbo_{i}.jpg', 'wb') as f:
        f.write(value)


if __name__ == '__main__':
    # redis信息
    # data_key = "image_test"
    host = "127.0.0.1"
    port = 6379
    db = 15

    print("-----------start-----------")
    def process_image(i):
        data_key = f"image_test_{i}"
        # t11 = time.time()
        value = get_data_from_redis(data_key, host, port, db)
        # print(f"单张图数据拉取时间：【{time.time() - t11:.4f}】秒")
        # decode_base64(value, i)
        decode_types(value, i)
        # decode_turbo(value, i)

    # pull
    pull_time_start = time.time()
    # po = ThreadPool(10)
    po = Pool(10)
    for i in range(300):
        po.apply_async(process_image, args=(i, ))
    po.close()
    po.join()
    pull_time_end = time.time()
    pull_time_cost = pull_time_end - pull_time_start
    print(f">>>>>> pull and decode 300 image cost time: {pull_time_cost:.4f} 秒")

