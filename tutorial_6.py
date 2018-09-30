import cv2 as cv
import numpy as np

#泛洪填充
def fill_color_demo(image):
    copyImg = image.copy()
    h, w = image.shape[:2]
    mask = np.zeros([h+2, w+2], np.uint8)
    cv.floodFill(copyImg, mask, (30,30), (255,0,255), (100,100,100), (50,50,50), cv.FLOODFILL_FIXED_RANGE)




src = cv.imread("D:/mytest/OpenCV/demo.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
fill_color_demo(src)
cv.waitKey(0)

cv.destroyAllWindows()
