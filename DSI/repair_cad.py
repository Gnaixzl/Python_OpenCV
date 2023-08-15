import numpy as np
import json
import cv2
import orjson
from scipy.spatial import KDTree


class ImageProcessor:
    def __init__(self):
        self.json_path = "front.json"
        self.output_path = "output_path"

    def load_json(self, path, pcb):
        '''
        函数功能介绍：加载json文件，解析出outline
        :param path: json文件的路径
        :param pab: 要解析的pcb名字
        :return: outline
        '''
        json_file = open(path, "r").read()
        wafer_json = orjson.loads(json_file)
        pcb_num = wafer_json[pcb]
        outline_all = []
        for pcb in pcb_num:
            outline = pcb["outline"]
            # newvalue = []
            # for item in outline:
            #     item = [int(item[0]), int(item[1])]
            #     newvalue.append(list(item))
            # print("1", type(outline))
            outline_all.append(outline)
        return outline_all

    def get_die_center(self, outline):
        '''
        函数功能介绍：获取每个die的中心坐标
        :param outline: 解析出的outline信息
        :return: 存放die中心点坐标的列表
        '''
        center = []
        # for i in range(len(outline)):
        #     outline_x.append(outline[i][0])
        #     outline_y.append(outline[i][1])
        # outline_x = sorted(outline_x)
        # outline_y = sorted(outline_y)
        # center_x = int((outline_x[2] - outline_x[0]) / 2 + outline_x[0])
        # center_y = int((outline_y[2] - outline_y[0]) / 2 + outline_y[0])
        outline = np.array(outline)
        # outline = outline.astype(np.int64)
        M = cv2.moments(outline)
        center_x = int(M['m10'] / M['m00'])
        center_y = int(M['m01'] / M['m00'])
        center.append(((center_x, center_y), outline))
        return center

    def die_distance(self, center1, center2):
        '''
        函数功能介绍：计算两个die之间的间距
        :param center1: 每列第一个die的中心点坐标
         :param center2: 每列最后一个die的中心点坐标
        :return: 两个die之间的间距
          '''
        # distance = (center2[0][1] - center1[0][1]) / 2
        distance = int(center2[0][0][0] - center1[0][0][0])
        return distance

    def get_circle_center(self, outline):
        '''
            函数功能介绍：获取每个circle的中心坐标
            :param outline: 解析出的outline信息
            :return: 存放circle中心点坐标的列表
        '''
        contours_circle = []
        center_circle = []
        for i in outline:
            contours_circle.append((i[0], i[1]))
        contours_circle_array = np.array(contours_circle, dtype=np.float32)
        # outline = np.array(outline)
        # outline = outline.astype(np.int64)
        ellipse = cv2.fitEllipse(contours_circle_array)
        center, axes, angle = ellipse
        cX = int(center[0])
        cY = int(center[1])
        center_circle.append(((cX, cY), outline))
        # print("center_circle = ", center_circle)
        return center_circle

    def circle_sorted(self, circle_on_die):
        '''
        函数功能介绍：对die中的小圆进行排序，按照先列从左到右、再行从上到下顺序
        :param center_list: 存放小圆中心点坐标的列表
        :return: 排序后的列表
        '''
        # squares_circle_1 = sorted(center_list, key=lambda x: x[0])
        # squares_circle_2 = []
        # squares_circle_3 = []
        # while squares_circle_1:
        #     x = squares_circle_1[0][0]
        #     for j in range(len(squares_circle_1)):
        #         if x - 0.09 <= squares_circle_1[j][0] <= x + 0.09:
        #             squares_circle_2.append(squares_circle_1[j])
        #     squares_circle_2 = sorted(squares_circle_2, key=lambda x: x[1])
        #     for k in squares_circle_2:
        #         squares_circle_1.remove(k)
        #     for (cX, cY) in squares_circle_2:
        #         squares_circle_3.append((cX, cY))
        #     squares_circle_2 = []
        # return squares_circle_3
        def sort_rule(point):
            return (point[0][0], point[0][1])
        sorted_circle = sorted(circle_on_die, key=sort_rule)
        return sorted_circle

    def get_center_all(self, center_die_all, center_circle_all):
        '''
        函数功能介绍：输入die的中心和circle的中心坐标，将die与circle配对，输出col_all=[(die_center,circle1_center,circle2_center,...),...]
        :param center_die_all: 存放die中心点坐标的列表
        :param center_circle_all: 存放circle中心点坐标的列表
        :return: 存放匹配后中心点坐标的列表，列表中的每个元素也是个列表
        '''
        center_all = []
        for c in center_die_all:
            # x_all = []
            # y_all = []
            # x_all.append(c[0][1][0][0])
            # x_all.append(c[0][1][1][0])
            # x_all.append(c[0][1][2][0])
            # x_all.append(c[0][1][3][0])
            # y_all.append(c[0][1][0][1])
            # y_all.append(c[0][1][1][1])
            # y_all.append(c[0][1][2][1])
            # y_all.append(c[0][1][3][1])
            # min_x = min(x_all)
            # max_x = max(x_all)
            # min_y = min(y_all)
            # max_y = max(y_all)
            min_x = c[0][0][0] - 387
            max_x = c[0][0][0] + 387
            min_y = c[0][0][1] - 389
            max_y = c[0][0][1] + 389
            circle_on_die = []
            for cnt in center_circle_all:
                if min_x < cnt[0][0][0] < max_x and min_y < cnt[0][0][1] < max_y:
                    circle_on_die.append(cnt)
            print("len(circle_on_die) = ", len(circle_on_die))
            sorted_circle = self.circle_sorted(circle_on_die)
            print("---len(sorted_circle) = ", len(sorted_circle))
            center_all.append((c, sorted_circle))
        return center_all

    def add_json_die(self, col_num, center_all, distance):
        '''
        函数功能介绍：补全每列轮廓信息
        :param col_num: 要进行补全的是第几列
        :param center_all: 存放每列头尾中心点的列表
        :param distance: 两个die之间的距离
        :return: 补全后的轮廓中心点列表集合
        '''
        col = []
        die_num = int((center_all[2 * col_num + 1][0][0][0][1] - center_all[2 * col_num][0][0][0][1]) / distance) - 1
        print("die_num = ", die_num)
        col.append(center_all[2 * col_num])
        # 补全die
        for i in range(die_num):
            center_below = []
            center_circle = []
            center_111 = []
            # center_below.append(((center_all[2 * col_num][0][0][0][0], center_all[2 * col_num][0][0][0][1] + (i + 1) * distance),
            #                      ((center_all[2 * col_num][0][0][1][0][0], center_all[2 * col_num][0][0][1][0][1] + (i + 1) * distance),
            #                       (center_all[2 * col_num][0][0][1][1][0], center_all[2 * col_num][0][0][1][1][1] + (i + 1) * distance),
            #                       (center_all[2 * col_num][0][0][1][2][0], center_all[2 * col_num][0][0][1][2][1] + (i + 1) * distance),
            #                       (center_all[2 * col_num][0][0][1][3][0], center_all[2 * col_num][0][0][1][3][1] + (i + 1) * distance))))
            for center in center_all[2 * col_num][0]:  # die
                # print("center_all[2 * col_num][0]", center_all[2 * col_num][0])
                die_outline = []
                # print("center[0][1] = ",center[1])
                for k in range(len(center[1])):
                    new_die = [center[1][k][0], int(center[1][k][1] + (i + 1) * distance)]
                    die_outline.append(new_die)
                center_below.append(((center[0][0], int(center[0][1] + (i + 1) * distance)), die_outline))
            # 补全circle
            for center in center_all[2 * col_num][1]:  # pad
                # print("center_all[2 * col_num][1]", center_all[2 * col_num][1])
                circle_outline = []
                for j in range(len(center[0][1])):
                    new_circle = [center[0][1][j][0], int(center[0][1][j][1] + (i + 1) * distance)]
                    circle_outline.append(new_circle)
                list_1 = []
                list_1.append(((center[0][0][0], int(center[0][0][1] + (i + 1) * distance)), circle_outline))
                center_circle.append(list_1)
            # center_111.append((center_below, center_circle))
            col.append((center_below, center_circle))
        # print("col = ", col)
        col.append(center_all[2 * col_num + 1])
        return col  # col = [[(die坐标),[(circle坐标),(),(),(),...]], [(die坐标),[(circle坐标),(),(),(),...]], ...]

    def processor(self, json_path):
        '''
        函数功能介绍：解析json文件、补全每列信息，存入到字典中
        :param json_path: json文件的路径
        :return: 存放die信息和circle信息的字典
        '''
        print("processor start...")
        col_all = []
        # 解析json、输出die的center
        print("get die center...")
        pcb_die = "PCBNUM_FRONT"
        center_die_all = []
        outline_die_all = self.load_json(json_path, pcb_die)
        for outline in outline_die_all:
            center = self.get_die_center(outline)
            center_die_all.append(center)
        # print("-----center_die_all[0] = ", center_die_all[0])
        # print("-----center_die_all[2] = ", center_die_all[2])
        distance = self.die_distance(center_die_all[0], center_die_all[2])
        # distance = 810.16
        print("distance = ", distance)
        # 解析json、输出circle的center
        print("get circle center...")
        pcb_circle = "CONNECTPAD_FRONT"
        center_circle_all = []
        outline_circle_all = self.load_json(json_path, pcb_circle)
        for outline in outline_circle_all:
            center = self.get_circle_center(outline)
            center_circle_all.append(center)
        # print("-----center_die_all[0] = ", center_die_all[0])
        # print("-----center_circle_all[0] = ", center_circle_all[0])
        # 将center_die与center_circle组合，输出到col_all
        center_all = self.get_center_all(center_die_all, center_circle_all)
        # print("-----center_all[0] = ", center_all[0])
        print("add col...")
        # 补全每列，i为列号
        n = int(len(center_all)/2)
        print("n = ", n)
        for i in range(n):
            col_all.append(self.add_json_die(i, center_all, distance))
        # print("-----col_all[0] = ", col_all[0])

        # 输出信息到die_dict和circle_dict中
        print("dict output...")
        die_dict = {}
        circle_dict = {}
        pic = 0
        for i in range(len(col_all)):
            for j in range(len(col_all[i])):
                # print("col_all[i] = ", col_all[i])
                # 输出die信息到字典
                # cx_die = col_all[i][j][0][0][0]
                # cy_die = col_all[i][j][0][0][1]
                key_die = (i, j)
                value_die = (col_all[i][j][0][0][0], pic, col_all[i][j][0][0][1])
                # print("value_die[2] = ", col_all[0][0][0][0][1])
                # print("value_die[0] = ", col_all[0][0][0][0][0])
                die_dict[key_die] = value_die  # key是列、行；value是中心坐标
                # 输出circle信息到字典
                for k in range(len(col_all[i][j][1])):
                    # cx_circle = col_all[i][j][1][k][0]
                    # cy_circle = col_all[i][j][1][k][1]
                    key_circle = (i, j, k)
                    # print("col_all[i][j][1][k][0] = ", col_all[i][j][1][k])
                    value_circle = (col_all[i][j][1][k][0][0], pic, col_all[i][j][1][k][0][1])
                    circle_dict[key_circle] = value_circle
                pic += 1
        return die_dict, circle_dict

    def output_json(self, die_dict, circle_dict):
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

        n = 0
        for i, (key, value) in enumerate(die_dict.items()):
            newvalue = []
            for item in value[2]:
                item = [int(item[0]), int(item[1])]
                newvalue.append(list(item))
            # json_dict['PCBNUM_FRONT'][i] = {'pic': int(value[1]), 'outline': newvalue, 'area': 4.5796000001, 'no': i, 'pt': list(value[0]), 'direction': 0.0, 'x': int(key[0]), 'y': int(key[1]), 'stripId': 0, 'isTemplate': 0, 'isBase': 1}
            json_list.extend([{'pic': int(value[1]), 'outline': newvalue, 'area': 4.5796000001, 'no': i,
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
            for item in value[2]:
                # if type(item) == 'int':
                # print("value[2] = ", value[2])
                item = [int(item[0]), int(item[1])]
                newvalue.append(list(item))
            # json_dict['CONNECTPAD_FRONT'][i] = {'pic': value[1], 'outline': newvalue, 'area': 0.000702681, 'no': i, 'pt':list(value[0]), 'direction': 0.0, 'x': key[0], 'y': key[1], 'z': key[2], 'stripId': 0, 'isTemplate': 0, 'isBase': 1}
            json_list.extend([{'pic': value[1], 'outline': newvalue, 'area': 0.000702681, 'no': i,
                                                'pt': list(value[0]), 'direction': 0.0, 'x': key[0], 'y': key[1],
                                                'z': key[2], 'stripId': 0, 'isTemplate': 0, 'isBase': 1}])
        json_dict['CONNECTPAD_FRONT'] = json_list


        # json_path = "Drawing3/front.json"
        # json_file = open(json_path, "r").read()
        # wafer_json = json.loads(json_file)
        # # print("json_dict = ", type(wafer_json))
        # # pcb_num = wafer_json['BASE_FRONT']
        # json_dict['BASE_FRONT'] = wafer_json['BASE_FRONT']

        print("json_dict = ", type(json_dict))
        with open('data/repair_output_front.json', 'w') as f:
            json.dump(json_dict, f)


if __name__ == '__main__':
    json_path = "data/output_front.json"
    processor = ImageProcessor()
    die_dict, circle_dict = processor.processor(json_path)
    # print("circle_dict = ", circle_dict)
    print("------------------------------------output json------------------------------------")
    processor.output_json(die_dict, circle_dict)

