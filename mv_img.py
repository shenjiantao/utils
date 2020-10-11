import os
from shen_utils.file_util import *
src_path='/data1/data/Plane/val/images'
dst_path='demo/val_scene/'
mkdir(dst_path)
while True:
    index=input('input img index')
    cmd='cp '+os.path.join(src_path,index+'.tif')+' '+dst_path
    print(cmd)
    os.system(cmd)