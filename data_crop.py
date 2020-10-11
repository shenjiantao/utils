import os
from xml.dom.minidom import Document
import numpy as np
import copy
import cv2
import sys
from shen_utils.file_util import *
sys.path.append('../../..')


def add_obj2objs(doc, objects, bbox, class_bbox, score_bbox):
    obj = doc.createElement('object')
    coord = doc.createElement('coordinate')
    coord_txt = doc.createTextNode('pixel')
    coord.appendChild(coord_txt)
    obj.appendChild(coord)

    type_obj = doc.createElement('type')
    type_obj_txt = doc.createTextNode('rectangle')
    type_obj.appendChild(type_obj_txt)
    obj.appendChild(type_obj)

    description = doc.createElement('description')
    description_txt = doc.createTextNode('None')
    description.appendChild(description_txt)
    obj.appendChild(description)

    possibleresult = doc.createElement('possibleresult')
    name = doc.createElement('name')
    name_txt = doc.createTextNode(class_bbox)
    name.appendChild(name_txt)
    possibleresult.appendChild(name)

    probability = doc.createElement('probability')
    probability_txt = doc.createTextNode(str(score_bbox))
    probability.appendChild(probability_txt)
    possibleresult.appendChild(probability)
    obj.appendChild(possibleresult)

    points = doc.createElement('points')
    for i in range(4):
        point = doc.createElement('point')
        point_txt = doc.createTextNode(str(bbox[2 * i]) + ',' + str(bbox[2 * i + 1]))
        point.appendChild(point_txt)
        points.appendChild(point)
    point = doc.createElement('point')
    point_txt = doc.createTextNode(str(bbox[0]) + ',' + str(bbox[1]))
    point.appendChild(point_txt)
    points.appendChild(point)
    obj.appendChild(points)
    objects.appendChild(obj)
    return objects



def save_to_xml(save_path, objects_axis, label_name):

    object_num = len(objects_axis)
    doc = Document()

    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)



    source = doc.createElement('source')
    filename = doc.createElement('filename')
    save_num=str(save_path.split('/')[-1].split('.')[0])
    filename_name = doc.createTextNode(save_num+'.tif')
    filename.appendChild(filename_name)
    source.appendChild(filename)
    orign=doc.createElement('orign')
    orign_text=doc.createTextNode('GF2/GF3')
    orign.appendChild(orign_text)
    source.appendChild(orign)

    annotation.appendChild(source)

    objects = doc.createElement('objects')
    annotation.appendChild(objects)

    for i in range(object_num):
        name=label_name[int(objects_axis[i][-1])]
        objects=add_obj2objs(doc,objects,objects_axis[i],name,1)

    f = open(save_path, 'w')
    f.write(doc.toprettyxml(indent=''))
    f.close()


class_list = ['Boeing737', 'Boeing747', 'Boeing777',
           'Boeing787', 'A220', 'A321', 'A330',
           'A350', 'ARJ21', 'other']


def format_label(txt_list):
    format_data = []
    for i in txt_list:
        if len(i.split(' ')) < 9:
            continue
        format_data.append(
            [float(xy) for xy in i.split(' ')[:8]] + [class_list.index(i.split(' ')[8].split('\n')[0])]
        )

        if i.split(' ')[8].split('\n')[0] not in class_list:
            print('warning found a new label :', i.split(' ')[8])
            exit()
    return np.array(format_data)


def clip_image(file_idx, image, boxes_all, width, height, stride_w, stride_h,save_dir):
    if len(boxes_all) > 0:
        shape = image.shape
        for start_h in range(0, shape[0], stride_h):
            for start_w in range(0, shape[1], stride_w):
                boxes = copy.deepcopy(boxes_all)
                box = np.zeros_like(boxes_all)
                start_h_new = start_h
                start_w_new = start_w
                if start_h + height > shape[0]:
                    start_h_new = shape[0] - height
                if start_w + width > shape[1]:
                    start_w_new = shape[1] - width
                top_left_row = max(start_h_new, 0)
                top_left_col = max(start_w_new, 0)
                bottom_right_row = min(start_h + height, shape[0])
                bottom_right_col = min(start_w + width, shape[1])

                subImage = image[top_left_row:bottom_right_row, top_left_col: bottom_right_col]

                box[:, 0] = boxes[:, 0] - top_left_col
                box[:, 2] = boxes[:, 2] - top_left_col
                box[:, 4] = boxes[:, 4] - top_left_col
                box[:, 6] = boxes[:, 6] - top_left_col

                box[:, 1] = boxes[:, 1] - top_left_row
                box[:, 3] = boxes[:, 3] - top_left_row
                box[:, 5] = boxes[:, 5] - top_left_row
                box[:, 7] = boxes[:, 7] - top_left_row
                box[:, 8] = boxes[:, 8]
                center_y = 0.25 * (box[:, 1] + box[:, 3] + box[:, 5] + box[:, 7])
                center_x = 0.25 * (box[:, 0] + box[:, 2] + box[:, 4] + box[:, 6])

                cond1 = np.intersect1d(np.where(center_y[:] >= 0)[0], np.where(center_x[:] >= 0)[0])
                cond2 = np.intersect1d(np.where(center_y[:] <= (bottom_right_row - top_left_row))[0],
                                       np.where(center_x[:] <= (bottom_right_col - top_left_col))[0])
                idx = np.intersect1d(cond1, cond2)
                if len(idx) > 0 and (subImage.shape[0] > 5 and subImage.shape[1] > 5):

                    mkdir(os.path.join(save_dir, 'images'))
                    img = os.path.join(save_dir, 'images',
                                       "%s_%04d_%04d.tif" % (file_idx, top_left_row, top_left_col))
                    cv2.imwrite(img, subImage)

                    mkdir(os.path.join(save_dir, 'label_xml'))
                    xml = os.path.join(save_dir, 'label_xml',
                                       "%s_%04d_%04d.xml" % (file_idx, top_left_row, top_left_col))
                    save_to_xml(xml, box[idx, :], class_list)

def data_crop(raw_data,save_dir,img_list,crop_size=800,stride=600):


    raw_images_dir = os.path.join(raw_data, 'images')
    raw_label_dir = os.path.join(raw_data, 'labelTxt')


    print('data split num:', len(img_list))


    for idx, img in enumerate(img_list):
        print(idx, 'read image', img)
        if not os.path.exists(os.path.join(raw_label_dir, img.replace('tif', 'txt'))):
            continue
        img_data = cv2.imread(os.path.join(raw_images_dir, img))

        txt_data = open(os.path.join(raw_label_dir, img.replace('tif', 'txt')), 'r').readlines()
        box = format_label(txt_data)
        clip_image(img.strip('.tif'), img_data, box, crop_size, crop_size, stride, stride,save_dir)

if __name__ == '__main__':
    #run xml2txt first
    raw_data = '/data1/user/plane_aug/train_split/'
    save_dir = '/data1/user/plane_aug/train_split/'
    img_list=[str(i)+'.tif' for i in range(1,1001)]
    # rmdir(save_dir)
    # mkdir(save_dir)
    data_crop(raw_data,save_dir,img_list,crop_size=800,stride=600)