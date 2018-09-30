import cv2 as cv
import numpy as np


src = cv.imread("D:/mytest/OpenCV/demo.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
print(src.shape)

#ROI操作
face = src[0:140, 120:260]
gray = cv.cvtColor(face, cv.COLOR_BGR2GRAY)

#因为原src图想为3通道图像，所以需要把gray变回3通道的图像backface，才能再赋值回src
backface = cv.cvtColor(gray, cv.COLOR_GRAY2BGR) #cv.COLOR_GRAY2BGR
src[0:140, 120:260] = backface
cv.imshow("face", src)
cv.waitKey(0)

cv.destroyAllWindows()
