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


def calculate_pipeline():
    pipelines = []
    start_time = time.time()
    grid_img = cv2.imread("data/1.jpg")
    jpg = jpg_encoderUtil().encode(grid_img, quality=95)
    image_base64 = base64.b64encode(jpg)
    # bytes_img = cv2.imencode('.jpg', grid_img)[-1].tobytes()
    for _ in range(10):
        # 在每个线程中创建独立的Pipeline对象
        pipeline = redis.Redis(host=host, port=port, db=db).pipeline()
        for i in range(30):
            data_key = f"image_test_{i + 30 * _}"
            pipeline.rpush(data_key, image_base64)
        # 将Pipeline对象添加到列表中
        pipelines.append(pipeline)
    po = ThreadPool(10)

    for j in range(10):
        po.apply_async(execute_pipeline, args=(pipelines[j], ))
    po.close()
    po.join()
    end_time = time.time()
    cost_time = end_time - start_time
    print(f">>>>>> types encode and push 300 image cost time: {cost_time:.4f} 秒")


def execute_pipeline(pipeline):
    t11 = time.time()
    pipeline.execute()
    print(f"单张图数据推送时间：【{time.time() - t11:.4f}】秒")


calculate_pipeline()

