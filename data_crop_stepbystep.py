
import os
import xml.etree.ElementTree as ET
from shen_utils.file_util import *
import numpy as np
from shen_utils.data_crop import data_crop
CLASSES = {'Boeing737':1, 'Boeing747':2, 'Boeing777':3,
           'Boeing787':4, 'A220':5, 'A321':6, 'A330':7,
           'A350':8, 'ARJ21':9, 'other':10}

def get_cls_num(xml_path):
    labels = []
    # don't use listdir for right order
    for xml in os.listdir(xml_path):
        xmlpath = os.path.join(xml_path, xml)
        root = ET.parse(xmlpath).getroot()
        objs = root.find('objects')
        label = []
        for obj in objs.findall('object'):
            possibleresult = obj.find('possibleresult')
            name = possibleresult.find('name').text
            label.append(CLASSES[name])
        labels.append(label)
    cls_img_num = np.zeros(10)
    for index, label in enumerate(labels):
        for i in range(1, 11):
            if i in label:
                cls_img_num[i - 1] += 1
    print('dst class img num', cls_img_num)
    print('all num ',len(labels))
    return cls_img_num


def get_cls_index(xml_path):
    labels = []
    # don't use listdir for right order
    for i in range(1, 1001):
        xmlpath = os.path.join(xml_path, str(i) + '.xml')
        root = ET.parse(xmlpath).getroot()
        objs = root.find('objects')
        label = []
        for obj in objs.findall('object'):
            possibleresult = obj.find('possibleresult')
            name = possibleresult.find('name').text
            label.append(CLASSES[name])
        labels.append(label)

    cls_img_num = np.zeros(10)
    cls_img_index = [[] for _ in range(10)]
    for index, label in enumerate(labels):
        for i in range(1, 11):
            if i in label:
                cls_img_num[i - 1] += 1
                cls_img_index[i - 1].append(index)
    print('src cls img num ',cls_img_num)
    return cls_img_index


if __name__ == '__main__':
    raw_data = '/data1/user/plane_aug/train'
    save_dir = '/data1/user/plane_aug/train_split_pytorch/'
    src_xml_path = '/data1/user/plane_aug/train/label_xml'
    dst_xml_path = '/data1/user/plane_aug/train_split_pytorch/label_xml'
    # ceshi_path='/data1/user/AerialDetection/test_result/result'
    print('befor crop')
    cls_img_index=get_cls_index(src_xml_path)
    crop_index=cls_img_index[-2]
    print(crop_index)
    crop_img_list=[ str(index+1)+'.tif' for index in crop_index]
    # data_crop(raw_data, save_dir, crop_img_list,crop_size=600,stride=400)
    #ARJ21 900,200;700,200;500,200;500,400;500,600;700,300
    #Boeing777 900,300;700,400;500,500;600,400
    print('after crop')
    cls_img_num= get_cls_num(dst_xml_path)