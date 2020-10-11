import numpy as np
import random
import cv2
import os
import tqdm
from DOTA_devkit.dota_utils import get_xml_object
from xml.dom.minidom import Document,parse
import xml.etree.ElementTree as ET

def get_iou(hbbox1,hbbox2):
    if hbbox2.ndim == 1:
        hbbox2 = hbbox2.reshape(-1,4)
    areas = np.zeros(shape=(len(hbbox1),len(hbbox2)))
    for i in range(len(hbbox1)):
        for j in range(len(hbbox2)):
            xmin = max(hbbox1[i][0],hbbox2[j][0])
            ymin = max(hbbox1[i][1],hbbox2[j][1])
            xmax = min(hbbox1[i][2],hbbox2[j][2])
            ymax = min(hbbox1[i][3],hbbox2[j][3])
            width = xmax - xmin
            height = ymax - ymin
            if width<=0 or height <=0:
                areas[i][j] = 0
            else:
                areas[i][j] = width*height
    return areas

def ploy2hbbox(ploy):
    bbox_x = [int(x) for (x, y) in ploy]
    bbox_y = [int(y) for (x, y) in ploy]
    min_x, max_x = max(min(bbox_x), 0), min(max(bbox_x), 1024)
    min_y, max_y = max(min(bbox_y), 0), min(max(bbox_y), 1024)
    hbbox = [min_x,min_y,max_x,max_y]
    return hbbox

def get_center_delta(ploy):
    hbbox = ploy2hbbox(ploy)
    w,h = hbbox[2]-hbbox[0],hbbox[3]-hbbox[1]
    center_x,center_y = int((hbbox[0]+hbbox[2])/2),int((hbbox[1]+hbbox[3])/2)
    delta_ploy = []
    for (x,y) in ploy:
        delta_ploy.append(center_x-x)
        delta_ploy.append(center_y-y)
    center = [center_x,center_y]
    scale = [w,h]
    return center,delta_ploy,scale

def random_xy(a,b):
    x = random.randrange(a,b)
    y = random.randrange(a,b)
    return x,y

def gener_new_bbox(center,scale):
    x1 = center[0] - int(scale[0]/2)
    x2 = center[0] + scale[0] - int(scale[0]/2)
    y1 = center[1] - int(scale[1]/2)
    y2 = center[1] + scale[1] - int(scale[1]/2)
    new_bbox_coord = [x1,y1,x2,y2]
    return np.array(new_bbox_coord)

def ploys2hbboxs(objs):
    hbboxs = []
    for obj in objs:
        hbbox=ploy2hbbox(obj['poly'])
        hbboxs.append(hbbox)
    return np.array(hbboxs)

def overlap(bboxs1,bbox2):
    x1 = bboxs1[:,0]
    y1 = bboxs1[:,1]
    x2 = bboxs1[:,2]
    y2 = bboxs1[:,3]

    left_top = (x1 < bbox2[0])* (bbox2[0] < x2)*(y1 < bbox2[1])*(bbox2[1] < y2)
    left_bottom = (x1 < bbox2[0])* (bbox2[0] < x2)*(y1 < bbox2[3])*(bbox2[3] < y2)
    right_top = (x1 < bbox2[2])* (bbox2[2] < x2)*(y1 < bbox2[1])*(bbox2[1] < y2)
    right_bottom = (x1 < bbox2[2])* (bbox2[2] < x2)*(y1 < bbox2[3])*(bbox2[3] < y2)
    if sum(left_top)+sum(left_bottom)+sum(right_top)+sum(right_bottom) > 0 :
        return True
    else:
        return False

def get_ori_coord(center,delta,zoom,angle):
    ori_coord = []
    assert len(delta) == 8
    assert angle == 0 or angle == 90 or angle == 180 or angle == 270
    if angle == 0 or angle == 180:
        for i in range(4):
            ori_coord.append(center[0] - int(delta[2*i] * zoom))
            ori_coord.append(center[1] - int(delta[2*i+1] * zoom))
    elif angle == 90 or angle ==270:
        for i in range(4):
            ori_coord.append(center[0] + int(delta[2*i+1] * zoom))
            ori_coord.append(center[1] - int(delta[2*i] * zoom))
    return ori_coord

def save_detections_xml(init_xml,class_name,bbox,dst_path):
    tree = parse(init_xml)
    doc = Document()
    root = tree.documentElement
    objects = root.getElementsByTagName('objects')[0]
    objects = add_obj2objs(doc,objects,class_name,bbox)
    with open(dst_path, 'wb') as f:
        f.write(tree.toprettyxml(indent='\t',newl="\n", encoding='utf-8'))
        f.close()

def add_obj2objs(doc,objects,class_name,bbox):

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
    name_txt = doc.createTextNode(class_name)
    name.appendChild(name_txt)
    possibleresult.appendChild(name)

    probability = doc.createElement('probability')
    probability_txt = doc.createTextNode(str(1))
    probability.appendChild(probability_txt)
    possibleresult.appendChild(probability)
    obj.appendChild(possibleresult)

    points = doc.createElement('points')
    for i in range(4):
        point = doc.createElement('point')
        point_txt = doc.createTextNode(str(bbox[2*i])+','+str(bbox[2*i+1]))
        point.appendChild(point_txt)
        points.appendChild(point)
    point = doc.createElement('point')
    point_txt = doc.createTextNode(str(bbox[0]) + ',' + str(bbox[1]))
    point.appendChild(point_txt)
    points.appendChild(point)
    obj.appendChild(points)
    objects.appendChild(obj)
    return objects

def change_xml_name(src_xml,det_xml,index):
    tree = ET.parse(src_xml)
    root = tree.getroot()
    source = root.find('source')
    filename = source.find('filename')
    filename.text = str(index)+'.bmp'
    tree.write(det_xml)

def tif2bmp(src_tif_img,det_bmp_img):
    tif_img = cv2.imread(src_tif_img)
    cv2.imwrite(det_bmp_img,tif_img)


for i in range(1,1001):
    src_xml = '/data1/user/plane_aug/train/label_xml/'+str(i)+'.xml'
    det_xml = '/data1/user/plane_aug/train_1010/label_xml/'+str(i)+'.xml'
    change_xml_name(src_xml,det_xml,i)

img_list = np.arange(1,1001)
img_list = tqdm.tqdm(img_list)
for i in img_list:
    src_tif = '/data1/user/plane_aug/train/images/'+str(i)+'.tif'
    det_bmp = '/data1/user/plane_aug/train_1010/images/'+str(i)+'.bmp'
    tif2bmp(src_tif,det_bmp)


'''
aug_num_dict = {'Boeing737':0, 'Boeing747':1, 'Boeing777':5,
               'Boeing787':1, 'A220':0, 'A321':1, 'A330':1,
               'A350':2, 'ARJ21':2, 'other':0}

list = tqdm.tqdm([i for i in range(1001,1011)])
for src_idx in list:
    src_img = cv2.imread('/data1/user/plane_aug/ARJ21/images/'+str(src_idx)+'.bmp')
    # src_img = cv2.imread('imgs/'+str(src_idx)+'.tif')
    src_objs = get_xml_object('/data1/user/plane_aug/ARJ21/label_xml/'+str(src_idx)+'.xml')
    # src_objs = get_xml_object('xmls/'+str(src_idx)+'.xml')

    src_objs_hbbox = ploys2hbboxs(src_objs)

    for obj in src_objs:
        count = 0
        name = obj['name']
        bbox = obj['poly']
        hbbox = ploy2hbbox(bbox)
        if np.min(hbbox) <= 0 or np.max(hbbox) >= 1024:
            continue
        aug_num = aug_num_dict[name]
        while count < aug_num:
            count += 1
            tar_idx = random.randrange(1001, 1011)
            tar_img_path = '/data1/user/plane_aug/ARJ21/images/'+str(tar_idx)+'.bmp'
            tar_xml_path = '/data1/user/plane_aug/ARJ21/label_xml/'+str(tar_idx)+'.xml'
            # tar_img_path = 'imgs/'+str(tar_idx)+'.tif'
            # tar_xml_path = 'xmls/'+str(tar_idx)+'.xml'
            tar_img = cv2.imread(tar_img_path)
            tar_objs = get_xml_object(tar_xml_path)
            tar_objs_hbbox = ploys2hbboxs(tar_objs)

            center,delta,scale = get_center_delta(bbox)
            boundary_min = max(100,max(delta))
            new_center = random_xy(boundary_min,1024-boundary_min)
            scale = [1.2*i for i in scale]
            new_bbox = gener_new_bbox(new_center,scale)
            iou = get_iou(tar_objs_hbbox,new_bbox)
            # print(sum(iou))
            if np.sum(iou) == 0:
                chip = src_img[hbbox[1]:hbbox[3],hbbox[0]:hbbox[2]]
                zoom = random.randrange(8, 13) / 10
                new_w,new_h = int((hbbox[2]-hbbox[0])*zoom),int((hbbox[3]-hbbox[1])*zoom)
                new_img = cv2.resize(chip,dsize=(new_w,new_h),interpolation=cv2.INTER_LINEAR)
                orient = random.randrange(0,4)
                if orient == 0:   # 0
                    new_img = new_img
                    ori_coord = get_ori_coord(new_center,delta,zoom,angle=0)
                elif orient == 1: # 90
                    new_img = np.rot90(new_img)
                    ori_coord = get_ori_coord(new_center, delta, zoom, angle=90)
                elif orient == 2: # 180
                    new_img = np.rot90(np.rot90(new_img))
                    ori_coord = get_ori_coord(new_center, delta, zoom, angle=180)
                elif orient == 3: # 270
                    new_img = np.rot90(np.rot90(np.rot90(new_img)))
                    ori_coord = get_ori_coord(new_center, delta, zoom, angle=270)
                tar_img_left_top = new_center[0] - int(new_w/2),new_center[1]-int(new_h/2)

                if orient == 0 or orient == 2:
                    tar_coord = [tar_img_left_top[0], tar_img_left_top[1], tar_img_left_top[0] + new_w,tar_img_left_top[1] + new_h]
                else:
                    tar_coord = [tar_img_left_top[0], tar_img_left_top[1], tar_img_left_top[0] + new_h,tar_img_left_top[1] + new_w]

                tar_img[tar_coord[1]:tar_coord[3], tar_coord[0]:tar_coord[2]] = new_img
                cv2.imwrite(tar_img_path,tar_img)
                save_detections_xml(tar_xml_path,name,ori_coord,tar_xml_path)


'''