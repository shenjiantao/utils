import numpy as np
import cv2
import os

# img_h, img_w = 32, 32
img_h, img_w = 1024,1024
means, stdevs = [], []
img_list = []
imgs_path_list=[]
train_path = '/data1/data/Plane/train/images/'
train_list = os.listdir(train_path)
for item in train_list:
    imgs_path_list.append(os.path.join(train_path, item))
val_path='/data1/data/Plane/val/images/'
val_list=os.listdir(val_path)
for item in val_list:
    imgs_path_list.append(os.path.join(val_path, item))
test_path = '/data1/user/test/images/'
test_list = os.listdir(test_path)
for item in test_list:
    imgs_path_list.append(os.path.join(test_path, item))


len_ = len(imgs_path_list)
i = 0
for item in imgs_path_list:
    print(item)
    img = cv2.imread(item)
    img = cv2.resize(img, (img_w, img_h))
    img = img[:, :, :, np.newaxis]
    img_list.append(img)
    i += 1
    print(i, '/', len_)

imgs = np.concatenate(img_list, axis=3)
imgs = imgs.astype(np.float32) / 255.

for i in range(3):
    pixels = imgs[:, :, i, :].ravel()  # 拉成一行
    means.append(np.mean(pixels))
    stdevs.append(np.std(pixels))

# BGR --> RGB ， CV读取的需要转换，PIL读取的不用转换
means.reverse()
stdevs.reverse()

print("normMean = {}".format(np.array(means)*255))
print("normStd = {}".format(np.array(stdevs)*255))
# mean=np.array([0.4581215, 0.4603336, 0.3802149])
# std=np.array([0.2017111, 0.1718912, 0.15873961])
#
# print(mean*255)
# print(std*255)
# img=cv2.imread('/data1/user/AerialDetection/results.jpg')
# print()