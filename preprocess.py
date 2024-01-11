# -*- coding: utf-8 -*-

import cv2
import numpy as np


def get_image(img_path, norm=True, rgb=True, nchw=False):
    img = cv2.imread(img_path)

    if img is None:
        raise FileNotFoundError('No such image: {}'.format(img_path))
    img_float = img.astype('float32')
    img_norm = img_float

    ## 如果提供的图片与模型输入图片大小不一致，这里需要设置大小并进行resize
    # resizeH, resizeW, resizeC = 640, 640, 3
    # img_norm = cv2.resize(img_float, (resizeW, resizeH), interpolation=cv2.INTER_LINEAR)

    ## 注意这里的顺序和input_config.ini 中的mean/std的顺序问题
    mean_BGR = [0.0, 0.0, 0.0]
    std_BGR = [255.0, 255.0, 255.0]
    if norm:
        img_norm = (img - mean_BGR) / std_BGR
        img_norm = img_norm.astype('float32')
    else:
        img_norm = np.round(img).astype('uint8')
    if rgb:
        img_norm = cv2.cvtColor(img_norm, cv2.COLOR_BGR2RGB)
    if nchw:
        img_norm = np.transpose(img_norm, axes=(2, 0, 1))  # HWC -> CHW

    return np.expand_dims(img_norm, 0)  # CHW -> NCHW


def image_preprocess(img_path, norm=True):
    return get_image(img_path, norm=norm)
