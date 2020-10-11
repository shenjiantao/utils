import os
import shutil
import numpy as np
import cv2
import pandas as pd
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
def rmdir(path):
    if  os.path.exists(path):
        shutil.rmtree(path)
def out_rect(bbox,img):
    x=[point[0] for point in bbox]
    y = [point[1] for point in bbox]
    x_min=np.min(x)
    y_min=np.min(y)
    x_max=np.max(x)
    y_max=np.max(y)
    roi=img[y_min:y_max,x_min:x_max]
    return roi
def write_excel(mat,path,columns=None,index=None):
    data = pd.DataFrame(mat)
    if columns is not None:
        data.columns=columns
    if index is not None:
        data.index=index
    writer = pd.ExcelWriter(path)
    data.to_excel(writer, 'page_1')
    writer.save()
    writer.close()