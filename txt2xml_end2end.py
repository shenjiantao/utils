import os
import datetime
import shutil
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
def rmdir(path):
    if  os.path.exists(path):
        shutil.rmtree(path)

def write_empty_txt(src_img_dir,src_txt_dir):
    mkdir(src_txt_dir)
    for img in os.listdir(src_img_dir):
        name=img.split('.')[0]
        txt_path=os.path.join(src_txt_dir,name+'.txt')
        f = open(txt_path, 'w')
        f.close()

def trans(ori_txt_path, trans_txt_path):
    ori_txt_list = os.listdir(ori_txt_path)
    trans_txt_list = os.listdir(trans_txt_path)
    for ori_txt in ori_txt_list:
        path_ori=os.path.join(ori_txt_path,ori_txt)
        ori_txt_each_line_list = open(path_ori).read().splitlines()
        ori_txt_cls = ori_txt.split('_')[1].split('.')[0]
        for trans_txt in trans_txt_list:
            path_trans=os.path.join(trans_txt_path,trans_txt)
            trans_txt_name = trans_txt[:-4]
            file = open(path_trans, 'a')

            for ori_txt_each_line in ori_txt_each_line_list:
                item = ori_txt_each_line.split(' ')
                if trans_txt_name == item[0]:
                    score = float(item[1])
                    if score < 0.01:
                        continue
                    else:
                        x4 = float(item[2])
                        y4 = float(item[3])
                        x3 = float(item[4])
                        y3 = float(item[5])

                        x2 = float(item[6])
                        y2 = float(item[7])
                        x1 = float(item[8])
                        y1 = float(item[9])



                        file.write("{0[0]},{0[1]},{0[2]},{0[3]},{0[4]},{0[5]},{0[6]},{0[7]},{1:.2f},{2}".format(
                            [x1, y1, x2, y2, x3, y3, x4, y4], score, ori_txt_cls,) + '\n')
            file.close()

def addoneline(ori_txt_path):
    count=0
    ori_txt_list = os.listdir(ori_txt_path)
    for ori_txt in ori_txt_list:
        path_ori=os.path.join(ori_txt_path,ori_txt)
        size = os.path.getsize(path_ori)
        if size == 0:
            count=count+1
            print('no object ',ori_txt)
            file = open(path_ori, 'a')
            file.write("0,0,0,0,0,0,0,0,0.1,other")
            file.close()
    print('no object num :',count)
def txt2xml(src_txt_dir,src_xml_dir):
    mkdir(src_xml_dir)
    date=datetime.datetime.now().strftime('%Y-%m-%d')
    for txt in os.listdir(src_txt_dir):
        name=txt.split('.')[0]
        gt = open(os.path.join(src_txt_dir,txt)).read().splitlines()

        xml_file = open((os.path.join(src_xml_dir,name+'.xml')), 'w')
        xml_file.write('<?xml version="1.0"?>\n')
        xml_file.write('<annotation>\n')
        xml_file.write('    <source>\n')
        xml_file.write('        <filename>' + name + '.tif' + '</filename>\n')
        xml_file.write('        <origin>GF2/GF3</origin>\n')
        xml_file.write('    </source>\n')
        xml_file.write('    <research>\n')
        xml_file.write('        <version>4.0</version>\n')
        xml_file.write('        <provider>163</provider>\n')
        xml_file.write('        <author>lijin</author>\n')
        xml_file.write('        <pluginname>Airplane Detection and Recognition</pluginname>\n')
        xml_file.write('        <pluginclass> Detection</pluginclass>\n')
        xml_file.write('        <time>'+date+'</time>\n')
        xml_file.write('    </research>\n')
        xml_file.write('    <objects>\n')

        # write the region of image on xml file
        for img_each_label in gt:
            spt = img_each_label.split(',')
            # 这里如果txt里面是以逗号‘，’隔开的，那么就改为spt = img_each_label.split(',')。
            xml_file.write('        <object>\n')
            xml_file.write('            <coordinate>pixel</coordinate>\n')
            xml_file.write('            <type>rectangle</type>\n')
            xml_file.write('            <description>plane</description>\n')
            xml_file.write('            <possibleresult>\n')
            xml_file.write('                <name>' + str(spt[9]) + '</name>\n')
            xml_file.write('                <probability>' + str(spt[8]) + '</probability>\n')
            xml_file.write('            </possibleresult>\n')
            xml_file.write('            <points>\n')
            xml_file.write('                <point>' + str(spt[0]) + ',' + str(spt[1]) + '</point>\n')
            xml_file.write('                <point>' + str(spt[2]) + ',' + str(spt[3]) + '</point>\n')
            xml_file.write('                <point>' + str(spt[4]) + ',' + str(spt[5]) + '</point>\n')
            xml_file.write('                <point>' + str(spt[6]) + ',' + str(spt[7]) + '</point>\n')
            xml_file.write('                <point>' + str(spt[0]) + ',' + str(spt[1]) + '</point>\n')
            xml_file.write('            </points>\n')
            xml_file.write('        </object>\n')
        xml_file.write('    </objects>\n')
        xml_file.write('</annotation>')




if __name__ == '__main__':
    src_img_dir = "/data1/data/Plane/val/images"
    root_dir='/home/user/shen/DOTA-DOAI/FPN_Tensorflow_Rotation/tools/test_dota/FPN_Res101D_plane_split'

    src_txt_dir = os.path.join(root_dir,"img_txt")
    src_xml_dir = os.path.join(root_dir,"img_xml")
    ori_txt_path=os.path.join(root_dir,'dota_res')
    rmdir(src_txt_dir)
    rmdir(src_xml_dir)
    print('clean old result completed')
    write_empty_txt(src_img_dir,src_txt_dir)
    print('write_empty_txt completed')
    trans(ori_txt_path, src_txt_dir)
    print('transform from class txt to image txt completed')
    addoneline(src_txt_dir)
    print('add one line completed')
    txt2xml(src_txt_dir,src_xml_dir)
    print('txt2xml completed')




