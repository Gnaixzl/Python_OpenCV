import cv2
import numpy as np
import os


def get_pos_by_template(img_src, target_pic, debug_status, val):
    """
    模板匹配，速度快，但唯一的缺点是，改变目标窗体后，必须重新截取模板图片才能正确匹配
    :param img_src:
    :param target_pic:
    :param debug_status:
    :param val:
    :return: 返回坐标(x,y) 与opencv坐标系对应，以及与坐标相对应的图片在模板图片中的位置
    """
    screen_width = img_src.shape[1]
    screen_high = img_src.shape[0]

    # 参数设置
    pos = None
    i = 0
    best_val = 0
    best_xy = None
    best_pos = None
    best_i = None
    # 开始匹配，并返回匹配度最高的模板
    print("------------------正在匹配...")
    for i in range(len(target_pic)):
        # print(i)
        pos, top_left, target_val = template_matching(img_src,
                                                      target_pic[i],
                                                      screen_width,
                                                      screen_high,
                                                      val,
                                                      debug_status,
                                                      i)
        if target_val > best_val:
            best_val = target_val
            best_xy = top_left
            best_pos = pos
            best_i = i
    print("匹配度最高的为第{}张，匹配值为：{}".format(best_i+1, best_val))
    # 绘制图
    if best_val != 0:
        draw_img = img_src.copy()
        img_tmp_height = target_pic[best_i].shape[0]
        img_tmp_width = target_pic[best_i].shape[1]
        if 1:  # 绘图
            bottom_right = (best_xy[0] + img_tmp_width, best_xy[1] + img_tmp_height)
            cv2.rectangle(draw_img, best_xy, bottom_right, 255, 2)
            cv2.circle(draw_img, best_pos, 2, (0, 255, 0), -1)
            cv2.imshow("draw_img", draw_img)
            cv2.waitKey(0)
    return best_pos, best_i+1


def template_matching(img_src, template, screen_width, screen_height, val, debug_status, i):
    """
    模板匹配
    :param img_src: 原图
    :param template: 模板图
    :param screen_width:
    :param screen_height:
    :param val:
    :param debug_status:
    :param i:
    :return:
    """
    if (img_src is not None) and (template is not None):
        img_tmp_height = template.shape[0]
        img_tmp_width = template.shape[1]  # 获取模板图片的高和宽
        img_src_height = img_src.shape[0]
        img_src_width = img_src.shape[1]  # 匹配原图的宽高
        res = cv2.matchTemplate(img_src, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 最小匹配度，最大匹配度，最小匹配度的坐标，最大匹配度的坐标

        if debug_status:
            print(f">>>第 [ {i + 1} ] 张图片，匹配分数：[ {round(max_val, 2)} ]")
        # if max_val >= val:  # 计算相对坐标(计算进原图的缩放比例)
            position = [int(screen_width / img_src_width * (max_loc[0] + img_tmp_width / 2)),
                        int(screen_height / img_src_height * (max_loc[1] + img_tmp_height / 2))]
            return position, max_loc, max_val
        # else:
        #     return None



def read_img(image_path):
    """
    读取待检测图
    :param image_path:
    :return:
    """
    img = cv2.imread(image_path)
    return img


def read_template_img(template_path):
    """
    读取所有模板图
    :param template_path:
    :return:
    """
    # 加载路径下所有模板图
    file_list = os.listdir(template_path)
    template_file_list = [f for f in file_list if f.endswith('.jpg')]
    template = []
    for a in template_file_list:
        template_name = template_path + a
        img = cv2.imread(template_name)
        template.append(img)
    print("template image num:{}".format(len(template)))
    return template


if __name__ == '__main__':
    # 参数配置
    img_path = "image/template_img/image_src/6.jpg"
    template_path = "image/template_img/template/"
    val = 0.8
    debug_status = True

    # 加载图像
    img_src = read_img(img_path)
    img_template = read_template_img(template_path)

    # 模板匹配
    position, pic_num = get_pos_by_template(img_src, img_template, debug_status, val)
    print("position:{}, pic_num:{}".format(position, pic_num))



