import cv2
import numpy as np

# 读取图像
img = cv2.imread('image/fruit.jpg')

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# 高斯滤波
gray_smooth = cv2.GaussianBlur(gray, (7, 7), 2)

# 计算梯度幅值
Canny_img = cv2.Canny(gray_smooth, 50, 150)
#
# # 显示原始图像和边缘图像
# cv2.imshow('Original Image', img)
# cv2.imshow('Edges', edges)
# cv2.imshow('gray_smooth', gray_smooth)
#
# # 等待用户按下键盘按钮
# cv2.waitKey(0)
#
# # 关闭所有窗口
# cv2.destroyAllWindows()


# Prewitt算子
kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=int)
x = cv2.filter2D(gray, cv2.CV_16S, kernelx)
y = cv2.filter2D(gray, cv2.CV_16S, kernely)
# 转uint8
absX = cv2.convertScaleAbs(x)
absY = cv2.convertScaleAbs(y)
Prewitt = cv2.addWeighted(absX, 0.8, absY, 0.8, 1)

# # 开运算
# kernel = np.ones((3, 3), np.uint8)
# opening = cv2.morphologyEx(Prewitt, cv2.MORPH_OPEN, kernel)
#
# # 闭运算
# kernel = np.ones((5, 5), np.uint8)
# closing = cv2.morphologyEx(Prewitt, cv2.MORPH_CLOSE, kernel)


# 显示原始图像和边缘图像
cv2.imshow('Prewitt', Prewitt)
cv2.imshow('Canny_img', Canny_img)
# cv2.imshow('opening', opening)

# 等待用户按下键盘按钮
cv2.waitKey(0)

# 关闭所有窗口
cv2.destroyAllWindows()

