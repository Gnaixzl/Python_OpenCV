import cv2 as cv
import numpy as np

#NumPy数组遍历每个像素点
def access_pixels(image):
    print(image.shape);
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    print("width : %s, height : %s, channels : %s"%(width,height,channels))
    for row in range(height):
        for col in range(width):
            for c in range(channels):
                pv = image[row, col, c]
                image[row, col, c] = 255 - pv
    cv.imshow("pixels_demo",image)

#像素取反
def inverse(image):
    dst = cv.bitwise_not(image)
    cv.imshow("pixels_demo",dst)

#创建图像
def create_image():

    img = np.zeros([400,400,3], np.uint8)
    img[: , : , 0] = np.ones([400,400])*255
    cv.imshow("new image", img)



src = cv.imread("D:/mytest/OpenCV/demo.jpg")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
cv.imshow("input image", src)
t1 = cv.getTickCount()
inverse(src)
t2 = cv.getTickCount()
time = (t2-t1)/cv.getTickFrequency();  #计算处理时间
print("time : %s ms"%(time*1000))
cv.waitKey(0)

cv.destroyAllWindows()
