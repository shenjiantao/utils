import os
import cv2
import sys
import shutil
import re
import numpy as np
import glob
import xml.etree.ElementTree as ET


def fn_draw(img, cls, x0, y0, x1, y1, x2, y2, x3, y3):
    #    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
    points = np.array([[x0, y0], [x1, y1], [x2, y2], [x3, y3]])
    cv2.polylines(img, [points], 1, (255, 0, 255))
    # 输入参数为图像、文本、位置、字体、大小、颜色数组、粗细
    cv2.putText(img, cls, (x3, y3), 1, 1, (0, 255, 0), 1)

def fn_draw2(img, cls, cls_index, cls_conf, x0, y0 , x1, y1, x2, y2, x3, y3):
#    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
    points = np.array([[x0,y0], [x1,y1], [x2,y2], [x3,y3]])
    color_list = [(0, 255, 0), (126, 126, 0), (126, 126, 255), (0, 126, 255), (0, 126, 126),
                  (0, 0, 126), (255, 0, 0), (255, 126, 0), (255, 255, 0), (255, 126, 126)]

    cv2.polylines(img, [points], 1, color_list[cls_index])
    # 输入参数为图像、文本、位置、字体、大小、颜色数组、粗细
    cv2.putText(img, cls + '_' + cls_conf, (x3, y3), 1, 1, (255,255,255), 1)


inputpath = "F:\\four_first\\test1\\"
outpath = "F:\\four_first\\test1_1012_1\\"
folder = os.path.exists(outpath)

if folder:
    shutil.rmtree(outpath)  # delete folder
    os.makedirs(outpath)  # makedirs
else:
    os.makedirs(outpath)  # makedirs

# read xml
shape_ann_dir = r'C:\\Users\\superlee\\Desktop\\ship_detection\\results\\1_50e_nest50_fpn_1012\\'
txt_Lists = glob.glob(shape_ann_dir + '\\*.txt')
print(len(txt_Lists))

# read path

class_set = set()
for tmp_file in txt_Lists:

    gt = open(tmp_file).read().splitlines()

    #txt_file = tmp_file.split('\\')[-1]
    # print(xml)
    #img_name = txt_file.replace('.txt', '.tif')


    # print(obj_num)
    for obj in gt:
        class_name_list = ["1", "2", "3", "4", "5"]
        spt = obj.split(" ")
        img_name = spt[0]
        class_name = spt[1]
        class_conf = spt[2]
        x0 = int(spt[3])
        y0 = int(spt[4])
        x1 = int(spt[5])
        y1 = int(spt[6])
        x2 = int(spt[7])
        y2 = int(spt[8])
        x3 = int(spt[9])
        y3 = int(spt[10])
        class_set.add(class_name)

        class_name_index = class_name_list.index(class_name)


        if os.path.exists(outpath + img_name):
            print(img_name)
            image = cv2.imread(outpath + img_name)
            # print(image)
        else:
            image = cv2.imread(inputpath + img_name)
        fn_draw2(image, class_name, class_name_index, class_conf, x0, y0, x1, y1, x2, y2, x3, y3)

        # save path
        cv2.imwrite(outpath + img_name, image)

print(class_set)
