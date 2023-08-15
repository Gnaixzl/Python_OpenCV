################################################################################
# task  : 检测实物图，对d轮廓排序，输出json
# input : 实物图（趟图）（旋转后）
# output: json包含轮廓信息
#
# process: 1.加载实物图，图像预处理
#          2.检查测die轮廓和pad轮廓
#          3.轮廓排序
#          4.存入字典 key = (x,y,z) value = (center,outline)
#          5.输出到json
#
# ps: 对于不同料，需要修改die和pad二值化阈值、修改长宽信息、修改die和pad面积用于筛选用
################################################################################

import numpy as np
import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2, 40).__str__()
import cv2
import time
import imutils
import math
import json
import statistics

class ImageProcessor:
    def __init__(self):
        self.img_path = "../../input/0427/0427_compose_1.png"
        self.output_path = "output_path"

    # 加载图片，绘制白板
    def load_img(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img, gray

    # # 根据轮廓信息得到外界矩形和其顶点坐标
    # def get_die_coordinate(self, contours):
    #     rect = cv2.minAreaRect(contours)
    #     box = cv2.boxPoints(rect)
    #     box = np.intp(box)
    #     x, y, width, height = cv2.boundingRect(box)
    #     return x, y, width, height, rect

    # 检测die轮廓
    def die_img_findcontours(self, gray):
        ret, thresh = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        # 根据面积筛选轮廓
        contours_die = []
        for index, c in enumerate(contours):
            if hierarchy[0][index][3] != -1:  # die外轮廓
                s = cv2.contourArea(c)
                if s >400000:
                    contours_die.append(c)
        return contours_die

    # 检测circle轮廓
    def circle_img_findcontours(self, gray):
        ret, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        # 根据面积筛选轮廓
        contours_circle = []
        circle_all = []
        for index, c in enumerate(contours):
            if hierarchy[0][index][3] == -1:  # pad内轮廓
                s = cv2.contourArea(c)
                if 2000 > s > 150:
                    contours_circle.append(c)
        for c in contours_circle:
            ellipse = cv2.fitEllipse(c)
            center, axes, angle = ellipse
            cX = int(center[0])
            cY = int(center[1])
            outline_c = []
            for i in range(len(c)):
                outline_c.append((c[i][0][0], c[i][0][1]))
            circle_all.append(((cX, cY), outline_c))
        return circle_all

    # 对squares_new位置进行排序，存入squares_new_sorted列表中，其中n代表die属于第几列
    def sorted_die(self, contours_die):
        die_dict = {}
        # 把轮廓center和outline组合为列表
        die_value = []
        for c in contours_die:
            # center_outline = []
            outline_die = []
            rect = cv2.minAreaRect(c)
            center_x = int(rect[0][0])
            center_y = int(rect[0][1])
            for i in range(len(c)):
                outline_die.append((c[i][0][0], c[i][0][1]))
            die_value.append(((center_x, center_y), outline_die))
            # print("-------die_value = ", die_value)
            # die_value.append(center_outline)
        # 根据center排序
        list_1 = sorted(die_value, key=lambda x: x[0][0])
        list_2 = []
        die_sorted = []
        col_num = 0
        while list_1:
            x = list_1[0][0][0]
            # print("x = ", x)
            for i in range(len(list_1)):
                if x - 20 <= list_1[i][0][0] <= x + 20:
                    list_2.append(list_1[i])
            for item in list_2:
                list_1.remove(item)
            list_2 = sorted(list_2, key=lambda x: x[0][1])
            for i, (center, outline) in enumerate(list_2):
                die_sorted.append((center, outline, col_num, i))  # col_num是列，i是行
            col_num += 1
            list_2 = []
        # print("---die_sorted = ", die_sorted)
        # print("---die_sorted[0][0] = ", die_sorted[0][0])
        # print("---die_sorted[0][2] = ", die_sorted[0][2])
        # 输出到字典dict_die
        for i in die_sorted:
            x = int(i[2])
            y = int(i[3])
            center = i[0]
            outline = i[1]
            key = (x, y)
            value = (center, outline)
            die_dict[key] = value
        return die_dict

    def sorted_circle(self, die_dict, contours_circle):
        dict_circle = {}
        for key, value in die_dict.items():
            x = value[0][0]
            y = value[0][1]
            # print("x,y = ", x, y)
            circle_on_die = []
            for c in contours_circle:
                # print("c[1] = ", c[1])
                outline_circle = []
                cX = c[0][0]
                cY = c[0][1]
                if x-420 < cX < x+420 and y-420 < cY < y+420:
                    # print("c[1] = ", c[1])
                    circle_on_die.append(((cX, cY), c[1]))
            # 对die里面的pad进行排序
            # print("circle_on_die = ", circle_on_die)
            print("len(circle_on_die) = ", len(circle_on_die))
            list_1 = sorted(circle_on_die, key=lambda x: x[0][0])
            list_2 = []
            circle_sorted = []
            circle_sorted_new = []
            while list_1:
                x = list_1[0][0][0]
                # print("x = ", x)
                for i in range(len(list_1)):
                    if x - 20 <= list_1[i][0][0] <= x + 20:
                        list_2.append(list_1[i])
                for item in list_2:
                    list_1.remove(item)
                list_2 = sorted(list_2, key=lambda x: x[0][1])
                for i, (center, outline) in enumerate(list_2):
                    circle_sorted.append((center, outline, key[0], key[1]))  # col_num是列，i是行
                list_2 = []
            for z, (center, outline, x, y) in enumerate(circle_sorted):
                circle_sorted_new.append((center, outline, x, y, z))
            # print("len(circle_sorted_new) = ", len(circle_sorted_new))
            # 输出到字典dict_circle
            for i in circle_sorted_new:
                x = int(i[2])
                y = int(i[3])
                z = int(i[4])
                center = i[0]
                outline = i[1]
                key = (x, y, z)
                value = (center, outline)
                dict_circle[key] = value
        return dict_circle


    def output_json(self,die_dict, circle_dict):
        '''
                函数功能介绍：根据补全的字典信息，输出json文件
                :param self:
                :param die_dict: die的信息（列，行）= {(cx,cy)}
                :param circle_dict: circle的信息（列、行、序号）= {(cx,cy)}
                :return: json output
                '''
        json_dict = {}
        json_dict['PCBNUM_FRONT'] = {}
        json_dict['CONNECTPAD_FRONT'] = {}
        json_dict['BASE_FRONT'] = {}
        json_list = []

        for i, (key, value) in enumerate(die_dict.items()):
            newvalue = []
            for item in value[1]:
                item = [int(item[0]), int(item[1])]
                newvalue.append(list(item))
            # json_dict['PCBNUM_FRONT'][i] = {'pic': int(value[1]), 'outline': newvalue, 'area': 4.5796000001, 'no': i, 'pt': list(value[0]), 'direction': 0.0, 'x': int(key[0]), 'y': int(key[1]), 'stripId': 0, 'isTemplate': 0, 'isBase': 1}
            json_list.extend([{'outline': newvalue, 'area': 4.5796000001, 'no': i,
                               'pt': list(value[0]), 'direction': 0.0, 'x': int(key[0]), 'y': int(key[1]),
                               'stripId': 0, 'isTemplate': 0, 'isBase': 1}])
        json_dict['PCBNUM_FRONT'] = json_list

        json_list = []
        for i, (key, value) in enumerate(circle_dict.items()):
            # print("value[2] = ", value[2])
            # print("value[2] = ", type(value[2]) == type(1))
            # if type(value[2]) == type(1):
            #     continue
            newvalue = []
            for item in value[1]:
                # if type(item) == 'int':
                # print("value[2] = ", value[2])
                item = [int(item[0]), int(item[1])]
                newvalue.append(list(item))
            # json_dict['CONNECTPAD_FRONT'][i] = {'pic': value[1], 'outline': newvalue, 'area': 0.000702681, 'no': i, 'pt':list(value[0]), 'direction': 0.0, 'x': key[0], 'y': key[1], 'z': key[2], 'stripId': 0, 'isTemplate': 0, 'isBase': 1}
            json_list.extend([{'outline': newvalue, 'area': 0.000702681, 'no': i,
                               'pt': list(value[0]), 'direction': 0.0, 'x': key[0], 'y': key[1],
                               'z': key[2], 'stripId': 0, 'isTemplate': 0, 'isBase': 1}])
        json_dict['CONNECTPAD_FRONT'] = json_list

        # json_path = "Drawing3/front.json"
        # json_file = open(json_path, "r").read()
        # wafer_json = json.loads(json_file)
        # # print("json_dict = ", type(wafer_json))
        # # pcb_num = wafer_json['BASE_FRONT']
        # json_dict['BASE_FRONT'] = wafer_json['BASE_FRONT']

        # print("json_dict = ", type(json_dict))
        # with open('data/0608_output/detect_output_0608.json', 'w') as f:
        with open('data/0620_output/test/0615_image_3.json', 'w') as f:
            json.dump(json_dict, f)


    # process函数
    def processor(self, img_path, compose_num):
        # 代表这是第几趟图
        compose_num = compose_num
        # 加载图
        print("load image...")
        load_img_start = time.time()
        img, gray = self.load_img(img_path)
        draw_img = img.copy()
        load_img_end = time.time()
        load_img_cost = load_img_end - load_img_start
        print(f"----load image cost time: {load_img_cost:.2f} 秒")

        # 检测die和circle轮廓
        print("findcontours...")
        findcontours_start = time.time()
        contours_die = self.die_img_findcontours(gray)
        contours_circle = self.circle_img_findcontours(gray)
        print("len(contours_die) = ", len(contours_die))
        print("len(contours_circle) = ", len(contours_circle))
        # cv2.drawContours(draw_img, contours_die, -1, (0, 0, 255), 2)
        # cv2.drawContours(draw_img, contours_circle, -1, (0, 0, 255), 2)
        # cv2.imshow("draw_img", draw_img)
        # cv2.waitKey(0)

        findcontours_end = time.time()
        findcontours_cost = findcontours_end - findcontours_start
        print(f"----findcontours cost time: {findcontours_cost:.2f} 秒")

        # 排序die，存入字典dict(x,y)={center,outline}
        print("sort die...")
        dict_die = self.sorted_die(contours_die)

        # 排序将pad与die匹配，并排序pad，存入字典dict(x,y,z)={center,outline}
        print("sort circle...")
        dict_circle = self.sorted_circle(dict_die, contours_circle)

        # 输出json
        self.output_json(dict_die, dict_circle)

        return dict_die, dict_circle




if __name__ == '__main__':
    # img_path = "data/0608_output/0608_rotation_image_1.png"
    img_path = "data/0615/1/3.jpg"
    processor = ImageProcessor()
    die_dict, circle_dict = processor.processor(img_path,1)
    # print("die_dict = ", die_dict)
    # print("circle_dict = ", circle_dict)
