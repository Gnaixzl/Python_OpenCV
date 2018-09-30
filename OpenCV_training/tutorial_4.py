import cv2 as cv
import numpy as np


#像素相加
def add_demo(m1, m2):
    dst = cv.add(m1, m2)
    cv.imshow("add_demo", dst)

#像素相减
def subtract_demo(m1, m2):
    dst = cv.subtract(m1, m2)
    cv.imshow("subtract_demo", dst)

#像素相乘
def multiply_demo(m1, m2):
    dst = cv.multiply(m1, m2)
    cv.imshow("multiply_demo", dst)

#像素相除
def divide_demo(m1, m2):
    dst = cv.divide(m1, m2)
    cv.imshow("divide_demo", dst)


src1 = cv.imread("D:/mytest/OpenCV/image/LinuxLogo.jpg")
src2 = cv.imread("D:/mytest/OpenCV/image/WindowsLogo.jpg")
print(src1.shape)
print(src2.shape)
cv.namedWindow("image1", cv.WINDOW_AUTOSIZE)
cv.imshow("image1", src1)
cv.imshow("image2", src2)

#add_demo(src1, src2)
#subtract_demo(src1, src2)
multiply_demo(src1, src2)
#divide_demo(src1, src2)
cv.waitKey(0)

cv.destroyAllWindows()
