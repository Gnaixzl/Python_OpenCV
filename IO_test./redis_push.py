import traceback
import cv2
import redis
import time
import sys
import os
import base64
from turbojpeg import TurboJPEG
import multiprocessing
from multiprocessing.pool import ThreadPool, Pool


def push_data_to_redis(put_redis, data, data_key):
    try:
        put_redis.rpush(data_key, data)
    except Exception as e:
        print(traceback.format_exc())


def jpg_encoderUtil():
    system = "linux"
    WORK_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    if system == "Windows":
        lib_path = os.path.join(WORK_PATH, "turbojpeg.dll")
    else:
        lib_path = os.path.join(WORK_PATH, "libturbojpeg.so")
    return TurboJPEG(lib_path=lib_path)


# redis信息
# data_key = "image_test"
host = "127.0.0.1"
port = 6379
db = 15


def process_image(grid_img, put_redis, i):
    data_key = f"image_test_{i}"

    # # base64 encode
    # jpg = jpg_encoderUtil().encode(grid_img, quality=95)
    # image_base64 = base64.b64encode(jpg)

    # bytes encode
    bytes_img = cv2.imencode('.jpg', grid_img)[-1].tobytes()

    # push
    push_data_to_redis(put_redis, bytes_img, data_key)


# 开启进/线程池
# po = Pool(10)
po = ThreadPool(10)

print("-----------start-----------")
grid_img = cv2.imread("data/1.jpg")

put111 = redis.ConnectionPool(host=host, port=port, password='', db=db)
put_redis = redis.Redis(connection_pool=put111)
start_time = time.time()
for i in range(300):
    po.apply_async(process_image, args=(grid_img, put_redis, i))
po.close()
po.join()

end_time = time.time()
cost_time = end_time - start_time
print(f">>>>>> types encode and push 300 image cost time: {cost_time:.4f} 秒")



