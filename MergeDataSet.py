import numpy as np
import cv2
import os
import glob
import shutil
from tqdm import tqdm

RawDirpath = './RawData/'
IntputDir = './InputData/'



output_jnt = os.path.join(IntputDir, 'jnt')
output_img = os.path.join(IntputDir, 'img')

if not os.path.exists(output_jnt):
    os.mkdir(output_jnt)
if not os.path.exists(output_img):
    os.mkdir(output_img)

Dirpathlist = os.listdir(RawDirpath)

DataIndex = 0

cv2.namedWindow("test")
Index = 0
for it in tqdm(Dirpathlist):

    Dirpathlist_temp = os.path.join(RawDirpath, it)
    la_dir = os.path.join(Dirpathlist_temp, 'jnt')
    la_list = glob.glob(la_dir + '/*.txt')
    la_list.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    for it in tqdm(la_list):
        img_temp = it.replace('jnt', 'img').replace('txt', 'png')


        out_img_path = os.path.join(os.path.join(output_img, str(Index) + '.png'))
        out_jnt_path = os.path.join(os.path.join(output_jnt, str(Index) + '.txt'))

        shutil.copy2(it, out_jnt_path)
        shutil.copy2(img_temp, out_img_path)
        Index = Index + 1