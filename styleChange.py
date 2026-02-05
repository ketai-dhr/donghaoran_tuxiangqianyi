# -*- coding:utf-8 -*-
import cv2
import time

def style_tupian(img, model_):
    # 读入图片，获取图片的宽度，高度
    # img = cv2.imread(pathin)
    (h, w) = img.shape[:2]
    model = model_ + ".t7"
    # 加载模型训练（图像处理）
    net = cv2.dnn.readNetFromTorch(r'./model/' + model)
    # 将图片构建，平均值像素点
    blob = cv2.dnn.blobFromImage(img, 1.0, (w, h), (103.939, 116.779, 123.680),
                                 swapRB=False, crop=False)
    net.setInput(blob)
    # 神经网络计算
    start = time.time()
    output = net.forward()
    end = time.time()
    print('风格迁移花费了{:.2f}秒'.format(end-start))
    # 图片正向拟合
    output = output.reshape((3,output.shape[2],output.shape[3]))
    output[0] += 103.939
    output[1] += 116.779
    output[2] += 123.680
    output = output.transpose(1,2,0)

    return output
