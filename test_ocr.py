import numpy as np
import os
import cv2
import paddlehub as hub


def process():
    pass



if __name__ == '__main__':
    # 参数设置
    img_path = "image/ocr_image/"
    file_list = os.listdir(img_path)
    img_list = [f for f in file_list if f.endswith('.jpeg')]

    # 开始识别
    ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")
    for i in img_list:
        img_name = img_path + i
        print("reading image : {}".format(img_name))
        np_images = cv2.imread(img_name)

        results = ocr.recognize_text(
            images=np_images,         # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
            use_gpu=False,            # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
            output_dir='image/ocr_result',  # 图片的保存路径，默认设为 ocr_result；
            visualization=True,       # 是否将识别结果保存为图片文件；
            box_thresh=0.5,           # 检测文本框置信度的阈值；
            text_thresh=0.5)          # 识别中文文本置信度的阈值；

        for result in results:
            data = result['data']
            save_path = result['save_path']
            for infomation in data:
                print('text: ', infomation['text'], '\nconfidence: ', infomation['confidence'], '\ntext_box_position: ',
                      infomation['text_box_position'])




