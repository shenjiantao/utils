import os
import xml.etree.ElementTree as ET
import random
import numpy as np

CLASSES = {'Boeing737':1, 'Boeing747':2, 'Boeing777':3,
           'Boeing787':4, 'A220':5, 'A321':6, 'A330':7,
           'A350':8, 'ARJ21':9, 'other':10}

labels=[]
xml_path='/data1/user/plane_aug/train/label_xml/'

def check(train_split,gt_labels):
    train_split=list(train_split)
    val_cls_split_num=np.zeros(10)
    train_split_label=gt_labels[train_split]
    for label in train_split_label:
        for i in range(1,11):
            if i in label:
                val_cls_split_num[i-1]+=1
    print(val_cls_split_num)


def split(labels):
    random.seed(10)
    train_split = set()

    cls_img_num = np.zeros(10)
    cls_img_index = [[] for _ in range(10)]
    for index, label in enumerate(labels):
        for i in range(1, 11):
            if i in label:
                cls_img_num[i - 1] += 1
                cls_img_index[i - 1].append(index)

    less2more = np.argsort(cls_img_num)  #class index from less to more
    select_num = [int(0.7 * (len(cls))) for cls in cls_img_index]
    # print('select 70% img', select_num)

    selected = set()
    for i in less2more:
        cls_img = cls_img_index[i]
        cls_img = list(set(cls_img) - selected)

        select = random.sample(cls_img, select_num[i])
        val = set(cls_img) - set(select)

        selected = selected | set(select) | val
        labels=np.array(labels)
        for label in labels[select]:
            for j in range(1, 11):
                if j in label:
                    select_num[j - 1] -= 1

        train_split = train_split | set(select)

    images_path = '/data1/user/plane_aug/train/images/'
    xml_path = '/data1/user/plane_aug/train/label_xml/'
    train_val_path = '/data1/user/plane_aug/train_val/'
    # os.mkdir(train_val_path)
    # os.mkdir(os.path.join(train_val_path,'images'))
    # os.mkdir(os.path.join(train_val_path,'label_xml'))
    # for image_index in train_split:
    #     os.system('cp ' + images_path + str(image_index+1) + '.tif  ' + train_val_path + 'train/images/')
    #     os.system('cp ' + xml_path + str(image_index+1) + '.xml  ' + train_val_path + 'train/label_xml/')
    # print(len(train_split))
    train_val=[i for i in range(1000)]
    val_split=set(train_val)-set(train_split)


    # for image_index in val_split:
    #     os.system('cp ' + images_path + str(image_index+1) + '.tif  ' + train_val_path + 'val/images/')
    #     os.system('cp ' + xml_path + str(image_index+1) + '.xml  ' + train_val_path + 'val/label_xml/')
    print('{:15}{}'.format('class img num', cls_img_num))
    print('{:15}'.format("train img num"),end='')
    check(train_split, labels)
    print('{:15}'.format("val img num"), end='')
    check(val_split,labels)

for i in range(1,1001):

    xmlpath=os.path.join(xml_path,str(i)+'.xml')
    root = ET.parse(xmlpath).getroot()
    objs = root.find('objects')
    label=[]
    for obj in objs.findall('object'):
        possibleresult = obj.find('possibleresult')
        name = possibleresult.find('name').text
        label.append(CLASSES[name])
    labels.append(label)

# print(len(labels))
split(labels)

