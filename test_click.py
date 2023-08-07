##########################
# 符合正太分布的随机点击脚本
##########################
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def click_mod(zoom=3, loc=0.0, scale=0.45, size=(2000, 2)):
    """
    生成正态分布的鼠标随机点击模型
    :param zoom:
    :param loc:
    :param scale:
    :param size:模型大小即模型中的坐标总量
    :return: 点集
    """
    # 随机生成呈正态分布的聚合坐标（坐标0,0 附近概率最高）
    mx, my = zip(*np.random.normal(loc=loc, scale=scale, size=size))

    # 对原始数据进行处理，点击模型除正态分布外，参照人类的眼动模型行为，点击规律还应呈现一定的长尾效应，所以对第二象限进行放大，对第四象限缩小
    x_int = []
    y_int = []
    for t in range(len(mx)):

        # 对第二象限的坐标放大
        if mx[t] < 0 < my[t]:
            x_int.append(mx[t] * zoom * 1.373)
            y_int.append(my[t] * zoom * 1.303)

        # 对第四象限的坐标缩小
        elif mx[t] > 0 > my[t]:

            # 若第四象限全部缩小，会导致第四象限的密度偏大，所以把其中三分之一的坐标，转换为第二象限的坐标（第二象限放大后密度会变小）
            roll = np.random.randint(0, 9)
            if roll < 5:  # 转换其中二分之一的坐标
                # pos = ClickModSet.pos_rotate([int(mx[t]), int(my[t])], 180)
                # x_int.append(int(pos[0]))
                # y_int.append(int(pos[1]))

                x_int.append(mx[t] * zoom * -1.350)
                y_int.append(my[t] * zoom * -1.200)

                # x_int.append(int(mx[i] * zoom * -1))
                # y_int.append(int(my[i] * zoom * -1))
            elif roll >= 8:  # 十分之二的坐标不处理
                x_int.append(mx[t] * zoom)
                y_int.append(my[t] * zoom)
            else:  # 剩下的坐标正常缩小
                x_int.append(mx[t] * zoom * 0.618)
                y_int.append(my[t] * zoom * 0.618)
        else:
            # 其他象限的坐标不变
            x_int.append(mx[t] * zoom)
            y_int.append(my[t] * zoom)

    # 处理边界问题，如果坐标点超出偏移范围，则缩小
    for t in range(len(x_int)):

        # # 先缩小，原始数据稍微超出了zoom的范围
        # x_int[t] = (x_int[t] * 0.816)
        # y_int[t] = (y_int[t] * 0.712)

        # 再判断是否超出边界，超出则再缩小超出的部分
        if abs(x_int[t]) > zoom:
            x_int[t] = (x_int[t] * 0.218)
        if abs(y_int[t]) > zoom:
            y_int[t] = (y_int[t] * 0.228)
        if (abs(x_int[t]) + abs(y_int[t])) > zoom * 1.55:
            x_int[t] = (int(x_int[t] * 0.218))
            y_int[t] = (int(y_int[t] * 0.228))

    # 合并数据
    mod_data = np.array(list(zip(x_int, y_int)))

    return mod_data


if __name__ == '__main__':
    mod_data = click_mod()
    # 数据可视化
    for i in range(len(mod_data)):
        plt.plot(mod_data[i][0], mod_data[i][1], 'o', color='red')
    plt.show()

