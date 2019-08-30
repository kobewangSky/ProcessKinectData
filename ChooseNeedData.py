import numpy as np
import cv2
import os
import glob
import shutil


def onkeyboard():
    print('onkeyboard')

def resetparam():
    label = open('./parameter.txt')
    parameter = label.read()

    parameter = parameter.split('\n')

    temp = []
    for parameter_it in parameter:
        temp.append(parameter_it.split(' '))
    global rvec, tvec, K, D
    rvec = np.array([[temp[0][0], temp[0][1], temp[0][2]]], np.float32)
    tvec = np.array([[temp[1][0], temp[1][1], temp[1][2]]], np.float32)
    K = np.array([temp[2][0:3], temp[2][3:6], temp[2][6:9]], np.float32)
    D = np.array([[temp[3][0]], [temp[3][1]], [temp[3][2]], [temp[3][3]]], np.float32)



    print('resetparam')


rvec = np.array([[1.5707964, -0.2, 0]], np.float32)
tvec = np.array([[-1.1, -3.4, 2]], np.float32)
K = np.array([[265.4047, 0, 649.17994], [0, 265.68588, 483.88972], [0,0,1]], np.float32)
D = np.array([[0.0896458], [-0.03444], [0.0065817], [-0.0187429]], np.float32)
resetparam()

InputDirpath = './InputData/'
OutputDir = './OutputData/'



output_jnt = os.path.join(OutputDir, 'jnt')
output_img = os.path.join(OutputDir, 'img')

if not os.path.exists(output_jnt):
    os.mkdir(output_jnt)
if not os.path.exists(output_img):
    os.mkdir(output_img)


cv2.namedWindow("test")
la_dir = os.path.join(InputDirpath, 'jnt')
la_list = glob.glob(la_dir + '/*.txt')
la_list.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

Index = 0
while Index <= len(la_list):

    la_temp = la_list[Index]
    img_temp = la_temp.replace('jnt', 'img').replace('txt', 'png')

    imgName = os.path.basename(img_temp)
    jntName = os.path.basename(la_temp)
    out_img_path = os.path.join(os.path.join(output_img, imgName))
    out_jnt_path = os.path.join(os.path.join(output_jnt, jntName))

    if os.path.exists(out_img_path) and os.path.exists(out_jnt_path):
        Index = Index + 1
        continue
    elif os.path.exists(out_img_path) or os.path.exists(out_jnt_path):
        assert False, 'output data error'

    label = open(la_temp)
    data = label.read()
    data = data.split('\n')
    img = cv2.imread(img_temp)

    XY_List = []

    for joint in data:
        if len(joint) < 4: continue
        point = joint.split(' ')
        print(point)
        XYZ = np.array([[[float(point[1]), float(point[2]), float(point[3])]]], np.float32)
        XY = cv2.fisheye.projectPoints(XYZ, rvec, tvec, K, D)[0][0][0]
        print(XY)
        if XY[0] < 0 or XY[1] < 0:
            XY[0] = -1
            XY[1] = -1
            XY_List.append(XY)
            continue
        else:
            XY_List.append(XY)


    cv2.circle(img, (XY_List[3][0], XY_List[3][1]), 3, (255, 0, 0))

    cv2.circle(img, (XY_List[4][0], XY_List[4][1]), 3, (0, 255, 0))
    cv2.circle(img, (XY_List[8][0], XY_List[8][1]), 3, (0, 255, 0))
    cv2.circle(img, (XY_List[6][0], XY_List[6][1]), 3, (0, 255, 0))
    cv2.circle(img, (XY_List[10][0], XY_List[10][1]), 3, (0, 255, 0))

    cv2.circle(img, (XY_List[12][0], XY_List[12][1]), 3, (0, 0, 255))
    cv2.circle(img, (XY_List[16][0], XY_List[16][1]), 3, (0, 0, 255))
    cv2.circle(img, (XY_List[14][0], XY_List[14][1]), 3, (0, 0, 255))
    cv2.circle(img, (XY_List[18][0], XY_List[18][1]), 3, (0, 0, 255))


    cv2.imshow("test", img)
    c = cv2.waitKey()
    if c == 100:
        shutil.copy2(img_temp, out_img_path)
        jntFile_out_file = open(out_jnt_path, "w")
        for jnt_data_ in XY_List:
            jntFile_out_file.write('{} {} \n'.format(jnt_data_[0], jnt_data_[1]))
        jntFile_out_file.close()
    elif c == 115:
        resetparam()
        continue
    Index = Index + 1