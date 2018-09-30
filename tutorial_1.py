import cv2 as cv
import numpy as np


def video_demo():
    #VideoCapture()函数打开视频文件，参数012代表摄像头，文件路径表示视频文件所在路径
    capture = cv.VideoCapture(0)
    while(True):
        ret, frame = capture.read()
        frame = cv.flip(frame, 1)
        cv.imshow("video",frame)
        c = cv.waitKey(50)
        if c == 27:
            break

def get_image_info(image):
    print(type(image))
    print(image.shape)
    print(image.size)
    print(image.dtype)
    pixel_data = np.array(image)
    print(pixel_data)


src = cv.imread("D:/mytest/OpenCV/demo.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
get_image_info(src)
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
cv.imwrite("D:/mytest/OpenCV/demo_1.jpg",gray)
cv.waitKey(0)

cv.destroyAllWindows()
