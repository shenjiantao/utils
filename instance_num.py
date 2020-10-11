from DOTA_devkit.dota_utils import get_xml_object
import os
import numpy as np
from shen_utils.file_util import *
CLASSES = ('Boeing737', 'Boeing747', 'Boeing777',
           'Boeing787', 'A220', 'A321', 'A330',
           'A350', 'ARJ21', 'other')
def read_xml(xml_path,instance_num):
    objects = get_xml_object(xml_path)
    for obj in objects:
        name = obj['name']
        instance_num[CLASSES.index(name)]+=1
    return instance_num


if __name__ == '__main__':
    # xml_path='/data1/data/Plane/train_aug65_bmp/label_xml/'
    # xml_path='/data1/user/plane_aug/train_split_bmp/label_xml'
    # xml_path='/data1/user/plane_aug/train/label_xml'
    xml_path = '/data1/data/Plane/train_aug_split_patch/label_xml'
    # xml_path = '/data1/user/plane_aug/train_1010/label_xml'
    instance_num=np.zeros(len(CLASSES))
    for xml in os.listdir(xml_path):
        instance_num=read_xml(os.path.join(xml_path,xml),instance_num)
    print(instance_num)
    write_excel(instance_num,'instance_num.xlsx',columns=['instance_num'],index=CLASSES)

