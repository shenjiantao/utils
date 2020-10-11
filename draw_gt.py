from shen_utils.file_util import *
from DOTA_devkit.dota_utils import get_xml_object

def draw_gt(img_path, xml_path, dstpath):
    global count
    img = cv2.imread(img_path)
    objects = get_xml_object(xml_path)
    for obj in objects:
        name = obj['name']
        bbox = obj['poly']

        green = (0,255,0)
        for i in range(3):
            cv2.line(img, bbox[i], bbox[i+1], color=green, thickness=2)
        cv2.line(img, bbox[3],bbox[0], color=green, thickness=2)
        cv2.putText(img, '%s' % name, (bbox[0][0], bbox[0][1] + 10),
                    color=green, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1)

    cv2.imwrite(dstpath, img)
if __name__ == '__main__':

    image_path = '../data_split/train_split/images'
    xml_save_path = '../data_split/train_split/label_xml'
    img_save_dir = '../demo/split_gt/'
    rmdir(img_save_dir)
    mkdir(img_save_dir)


    # for index in range(1, 4226):
    #     draw_gt(os.path.join(image_path, str(index) + '.tif'), os.path.join(xml_save_path, str(index) + '.xml'),
    #             os.path.join(img_save_dir, str(index) + '.jpg'))
    for f in os.listdir(image_path):
        draw_gt(os.path.join(image_path,f),os.path.join(xml_save_path,f.split('.')[0]+'.xml'),
                os.path.join(img_save_dir,f.split('.')[0]+'.png'))