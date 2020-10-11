from shen_utils.file_util import *
import datetime
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
            spt = img_each_label.split(' ')
            # spt=np.array(spt)
            # 这里如果txt里面是以逗号‘，’隔开的，那么就改为spt = img_each_label.split(',')。
            xml_file.write('        <object>\n')
            xml_file.write('            <coordinate>pixel</coordinate>\n')
            xml_file.write('            <type>rectangle</type>\n')
            xml_file.write('            <description>plane</description>\n')
            xml_file.write('            <possibleresult>\n')
            xml_file.write('                <name>' + str(spt[8]) + '</name>\n')
            xml_file.write('                <probability>' + '1' + '</probability>\n')
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

txt_path='/data1/user/plane_aug/train_rotate/labelTxt/'
xml_path='/data1/user/plane_aug/train_rotate/label_xml/'
# txt_path='/data1/data/Plane/train_aug/train_aug_rotate/labelTxt/'
# xml_path='/data1/data/Plane/train_aug/train_aug_rotate/label_xml/'
txt2xml(txt_path,xml_path)