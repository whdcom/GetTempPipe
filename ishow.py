# 王晗东
# 开发时间 2022/6/20 16:30
import cv2
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


def ishow(data):
    list = []
    arr = data.split(',')
    list.append(arr)
    list = np.array(list)
    list = list.astype(int)
    list = np.array(list).reshape((192, 256))
    print("Parsed message:", list)

    plt.imshow(list,interpolation=None,cmap=plt.cm.gray,origin='upper')
    plt.colorbar()
    plt.axis('off')
    plt.show()