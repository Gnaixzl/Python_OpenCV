import threading
import time
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import base64

import cv2
import requests
import multiprocessing
from multiprocessing.pool import ThreadPool, Pool
from turbojpeg import TurboJPEG
from datetime import datetime


def jpg_encoderUtil():
    system = "Linux"
    WORK_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    if system == "Windows":
        lib_path = os.path.join(WORK_PATH, "turbojpeg.dll")
    else:
        lib_path = os.path.join(WORK_PATH, "libturbojpeg.so")
    return TurboJPEG(lib_path=lib_path)


def encode_and_push_image(image):
    # encode
    # jpg = jpg_encoderUtil().encode(image, quality=95)
    # image_base64 = base64.b64encode(jpg)
    bytes_img = cv2.imencode('.jpg', image)[-1].tobytes()

    # push
    url = 'http://192.168.16.209:11007/apiJava/file/testUploadFile'
    image_data = {'file': bytes_img}
    response = requests.post(url, files=image_data)
    if response.status_code == 200:
        # print("image push success!")
        pass
    else:
        print(f"failed to push image!status_code = (response.status_code]")

if __name__ == '__main__':
    image = cv2.imread("data/1.jpg")

    # po = Pool(10)
    po = ThreadPool(10)

    print(f"start time = {dt}")
    start = time.time()
    for i in range(300):
        po.apply_async(encode_and_push_image, args=(image, ))
    po.close()
    po.join()
    end = time.time()
    print(f">>>>>> cost time = {end - start}")
    print(f"end time = {end}")

