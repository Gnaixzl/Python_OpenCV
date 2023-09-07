import socket
import base64
import struct
import time

import numpy as np
import os
import sys
import cv2
from turbojpeg import TurboJPEG
import multiprocessing
from multiprocessing.pool import ThreadPool, Pool
import threading


def jpg_encoderUtil():
    system = "Linux"
    WORK_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
    if system == "Windows":
        lib_path = os.path.join(WORK_PATH, "turbojpeg.dll")
    else:
        lib_path = os.path.join(WORK_PATH, "libturbojpeg.so")
    return TurboJPEG(lib_path=lib_path)


def decode_image(image_data):
    # Decode base64 image data
    # 保存图像
    # with open(f"out/socket_image_base64.jpg", "wb") as f:
    #     f.write(base64.b64decode(image_data))

    # # decode types
    # # jpg_data = jpg_encoderUtil().decode(image_data)
    with open('out/socket_image_types.jpg', 'wb') as f:
        f.write(image_data)

    # with open('out/socket_image_turbo.jpg', 'wb') as f:
    #     f.write(image_data)


def handle_client(client_socket):
    # 接收数据，一次接收8192字节，循环接收直到够一张图大小
    total_data = b''
    bytes_received = 0
    t1 = time.time()
    while bytes_received < 16921758:
        image_data = client_socket.recv(8192)
        # print(f"len(image_data) = {len(image_data)}")
        total_data += image_data
        bytes_received += len(image_data)

    # total_data = client_socket.recv(3488969)
    t2 = time.time()
    print(f"单次传输时间：{t2 - t1:.4f}秒")
    # 解码数据并保存
    decode_image(total_data)
    print(f"单次存图时间：{time.time() - t2:.4f}秒")
    print(f">>>>>> 单次总耗时时间：{time.time() - t1:.4f}秒")

    # Close socket
    client_socket.close()


def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(('127.0.0.1', 9999))

    # Listen for incoming connections
    server_socket.listen(10)

    # Create a process pool
    po = Pool(10)
    # po = ThreadPool(10)

    while True:
        # Accept a client connection
        client_socket, address = server_socket.accept()

        # Handle the client connection in a separate process
        po.apply_async(handle_client, (client_socket,))


if __name__ == '__main__':
    start_server()


