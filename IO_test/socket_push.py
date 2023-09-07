import socket
import base64
import struct
import time

import numpy as np
import os
import sys
import cv2
from turbojpeg import TurboJPEG
from multiprocessing.pool import ThreadPool, Pool


def jpg_encoderUtil():
    system = "Linux"
    WORK_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    if system == "Windows":
        lib_path = os.path.join(WORK_PATH, "turbojpeg.dll")
    else:
        lib_path = os.path.join(WORK_PATH, "libturbojpeg.so")
    return TurboJPEG(lib_path=lib_path)


def encode_and_push_image(image):
    print(f"-----encode_and_push_image start-----")
    tt = time.time()
    # 图像编码-TurboJPEG
    # jpg = jpg_encoderUtil().encode(image, quality=95)
    # print(f"len(TurboJPEG) = {len(jpg)}")
    # 图像编码-base64
    # image_base64 = base64.b64encode(jpg)

    # # # 图像编码-types
    bytes_img = cv2.imencode('.jpg', image)[-1].tobytes()

    # jpg_data = jpg_encoderUtil().decode(jpg)
    # with open('1111.jpg', 'wb') as f:
    #     f.write(jpg)

    # socket服务
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.16.246', 11112))

    # 发送数据
    s.sendall(bytes_img)
    print(f"单张图总耗时时间 : 【{time.time() - tt:.4f}】秒")
    # 关闭socket
    s.close()


def main():
    print(f"-----start-----")
    # 线程池
    # po = ThreadPool(10)
    # 进程池
    po = Pool(10)

    # 读图
    grid_img = cv2.imread("data/2.jpg")

    start_time = time.time()
    # 循环推图
    for i in range(50):
        po.apply_async(encode_and_push_image, args=(grid_img, ))
        # time.sleep(0.019)
    po.close()
    po.join()

    end_time = time.time()
    cost_time = end_time - start_time
    print(f">>>>>> encode and socket push cost time: {cost_time:.4f} 秒")


if __name__ == '__main__':
    main()


