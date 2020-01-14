import cv2 as cv
import numpy as np
import os
import sys
import random
import natsort
from xml.etree.ElementTree import Element, SubElement, ElementTree


# 샘플이미지 저장할 리스트
sample_img_list = []
# 샘플이미지에서 손으로 지정한 roi 저장할 리스트
roi_list = []

# template matching 에 사용될 이미지 리스트
template_img = []

def select_sample(img_list, sample_num = 5):
    '''
    img_list에서 sample을 선택!
    첫 번째 프레임은 반드시 선택되고, 나머지 자리는 랜덤으로 뽑힌다.
    '''
    global sample_img_list
    list_len = len(img_list)
    sample_img_list = [img_list[0]]    
    opening = sample_num - 1
    
    while True:
        r = random.randint(1, list_len - 1)
        if img_list[r] not in sample_img_list:
            sample_img_list.append(img_list[r])
            opening -= 1
        if opening == 0:
            print("sample 추출 완료!", sample_img_list)
            break
    
    
    return sample_img_list


def make_xml(img_name, img_folder, img_path, xml_file_path, min_point, max_point, label):
    '''
    labelImg 기본옵션으로 사용한 결과와 똑같이 나오도록 구현
    
    img_name = '*.jpg'  -> sample_img_list에 들어있음
    img_folder = '이미지가 들어있는 폴더이름' 
    img_path = 이미지를 포함한 절대 경로 예) /home/junsoofeb/models/research/images/train/000001.jpg 
    min_point = [[x, y]] 형태라서 받아올 때, 언패킹했음!
    max_point = [[x, y]] 형태라서 받아올 때, 언패킹했음!
    label = 지정할 label 
    '''
    
    img = cv.imread(img_path)
    img_shape = img.shape 
    #print(img_shape)
    #img_shape[0] == h
    #img_shape[1] == w
    #img_shape[2] == c
    

    root = Element('annotation')
    SubElement(root, 'folder').text = img_folder
    SubElement(root, 'filename').text = img_name
    SubElement(root, 'path').text = img_path
    source = SubElement(root, 'source')
    SubElement(source, 'database').text = 'Unknown'

    size = SubElement(root, 'size')
    SubElement(size, 'width').text = str(img_shape[0])
    SubElement(size, 'height').text = str(img_shape[1])
    SubElement(size, 'depth').text = str(img_shape[2])

    SubElement(root, 'segmented').text = '0'

    obj = SubElement(root, 'object')
    SubElement(obj, 'name').text = label
    SubElement(obj, 'pose').text = 'Unspecified'
    SubElement(obj, 'truncated').text = '0'
    SubElement(obj, 'difficult').text = '0'
    bbox = SubElement(obj, 'bndbox')
    SubElement(bbox, 'xmin').text = str(min_point[0])
    SubElement(bbox, 'ymin').text = str(min_point[1])
    SubElement(bbox, 'xmax').text = str(max_point[0])
    SubElement(bbox, 'ymax').text = str(max_point[1])                                                        

    tree = ElementTree(root)
    
    img_name = img_name.split('.')[0]
    tree.write(xml_file_path + img_name +'.xml')
    print(img_name +'.xml' + ' 생성 완료!')



# 아래 2줄의 G_img와 G_copy는 단순히 초기화 용도! 
G_img = np.zeros((1,1))
G_copy = G_img.copy()
moues_pressed = False
s_x = s_y  = e_x = e_y = -1
def mouse_callback(event, x, y, flags, param):
        global G_img, G_copy, s_x, s_y, e_x, e_y, moues_pressed
        if event == cv.EVENT_LBUTTONDOWN:
            moues_pressed = True
            s_x, s_y = x, y
            G_img = G_img.copy()

        elif event == cv.EVENT_MOUSEMOVE:
            if moues_pressed:
                G_copy = G_img.copy()
                cv.rectangle(G_copy, (s_x, s_y), (x, y), (0, 255, 0), 3)

        elif event == cv.EVENT_LBUTTONUP:
            moues_pressed = False
            e_x, e_y = x, y

def hand_labeling(img, i):
    '''
    img_list에 있는 이미지들을 손으로 수동 라벨링 작업!
    마우스로 드래그 후 'w'를 눌러서 라벨링! 
    '''
    global G_img, G_copy, s_x, s_y, e_x, e_y, moues_pressed, sample_img_list
    w, h = img.shape[0], img.shape[1]
    G_copy = img.copy()
    G_img = img.copy()
    roi = img.copy()
    
    min_point_list = []
    max_point_list = []
    

    cv.namedWindow("Press 'w' to label the image!")
    cv.setMouseCallback("Press 'w' to label the image!", mouse_callback)    
    while True:
        cv.imshow("Press 'w' to label the image!", G_copy)
        key = cv.waitKey(1)

        if key == ord('w'):
            if s_y > e_y:
                s_y, e_y = e_y, s_y
            if s_x > e_x:
                s_x , e_x = e_x, s_x

            if e_y - s_y > 1 and e_x - s_x > 0:
                cv.rectangle(G_copy, (s_x, s_y), (e_x, e_y), (0, 0, 255), 3)
                min_point_list.append([s_x, s_y])
                max_point_list.append([e_x, e_y])
                roi = roi[s_y:e_y, s_x:e_x]
                roi_list.append((roi))
                #index = sample_img_list[i]
                #cv.imwrite(f"/home/junsoofeb/auto_labeling/annotations/{index}", G_copy)
                break
        
        # 박스 그리기 실수 했을 경우 esc누르면 다시 시작.
        elif key == 27:
            G_copy = G_img.copy()
            continue
        
    cv.destroyAllWindows()
    
    return min_point_list, max_point_list



def main():
    # label 지정
    label = 'PET'
    
    # 라벨링 할 이미지 파일이 들어있는 폴더의 경로
    # /home/junsoofeb/auto_labeling/images/sample_1/*.jpg 인 경우
    img_file_path = "/home/junsoofeb/auto_labeling/images/sample_1/"
    
    # xml 파일이 저장될 경로
    xml_file_path = "/home/junsoofeb/auto_labeling/annotations/"
    
    # img_file_path에서 이미지가 들어있는 폴더 추출
    img_folder = img_file_path.split('/')[5]
    #print(img_folder)
    
    # 전체 이미지 목록받고, 오름차순 정렬
    img_list = os.listdir(img_file_path)
    img_list = natsort.natsorted(img_list)
    
    # template matching 수행할 샘플 이미지 선택하고, 수동 labeling 및 저장
    sample_img_list = select_sample(img_list, sample_num = 3)
    
    for i, img in enumerate(sample_img_list):
        G_img = cv.imread(f"/home/junsoofeb/auto_labeling/images/sample_1/{img}")
        min_point_list, max_point_list = hand_labeling(G_img, i)
        make_xml(img, img_folder, img_file_path + img, xml_file_path, *min_point_list, *max_point_list, label)
        

main()
    