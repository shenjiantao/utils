import os
import xml.etree.ElementTree as ET
import argparse
from shen_utils.file_util import *
def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='xml2txt demo')
    parser.add_argument('--txt','-T', dest='txt_path', help='txt path to save',
                        default='/data1/user/plane_aug/train_split/labelTxt')
    parser.add_argument('--Annotations','-A', dest='xml_path', help='xml path to read',
                        default='/data1/user/plane_aug/train_split/label_xml')
    args = parser.parse_args()

    return args

args=parse_args()

xml_path = args.xml_path


xml_list = os.listdir(xml_path)
rmdir(args.txt_path)
mkdir(args.txt_path)
for tmp_file in xml_list:
  with open(os.path.join(args.txt_path,tmp_file.replace(".xml", ".txt")), "w") as new_f:
    xmlpath=os.path.join(args.xml_path,tmp_file)
    root = ET.parse(xmlpath).getroot()
    objs = root.find('objects')
    for obj in objs.findall('object'):
        possibleresult = obj.find('possibleresult')
        name = possibleresult.find('name').text
        point_list = []
        points = obj.find('points')
        for point in points.findall('point'):
            point_list.append(point.text)
        x1, y1 = float(point_list[0].split(',')[0]), float(point_list[0].split(',')[1])
        x2, y2 = float(point_list[1].split(',')[0]), float(point_list[1].split(',')[1])
        x3, y3 = float(point_list[2].split(',')[0]), float(point_list[2].split(',')[1])
        x4, y4 = float(point_list[3].split(',')[0]), float(point_list[3].split(',')[1])
        difficult = str(0)
        new_f.write("{0[0]} {0[1]} {0[2]} {0[3]} {0[4]} {0[5]} {0[6]} {0[7]} {1} {2}\n".format([
            x2, y2, x1, y1, x4, y4, x3, y3], name, difficult))

print("Conversion completed!")

