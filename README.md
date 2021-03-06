# AUTO_labeling_project

## 1. 개요

동영상에서 이미지를 추출한 경우, 비슷한 이미지를 수동으로 labeling하는 것이 비효율적이기 때문에,  
자동으로 labeling을 해주고 xml파일을 생성해주는 프로그램 개발. 
(auto_labeling_v1.py)

#### 머그컵 labeling test video
#### 빨간 사각형은 xml file에 저장될 x_min, y_min, x_max, y_max 값으로 그린 사각형

[![youtube영상](![img000001](https://user-images.githubusercontent.com/46870741/72448102-d77e8980-37f9-11ea-8499-3804fb5c35fa.jpg)](https://www.youtube.com/watch?v=zoCb9Vpmg80)


## 2. 구현 환경

1) ubuntu 18.04
2) Python 3.6
3) OpenCV-python 4.2.0
4) Numpy 1.17

## 3. dataset 준비

### 동영상에서 추출한 이미지가 입력 데이터!

#### 동영상에서 이미지 추출은 ffmpeg 사용하면 편리, 사용법은 아래 링크 참고!  
<https://junsoofeb.github.io/posts/icrawl-3/>

머그컵 labeling test에서는 약 24초 분량의 동영상에서 초당 30 frame으로 이미지를 추출하여 사용하였다. (726장 추출)  
페트병 labeling test에서는 약 10초 분량의 동영상에서 초당 20 frame으로 이미지를 추출하여 사용하였다. (188장 추출)  


## 4. auto_labeling_v1.py  동작 과정

1) 사용자가 label, 이미지파일이 들어있는 폴더의 경로, xml파일이 저장될 경로 등을 지정한다.   
2) 첫 번째 이미지는 사용자가 마우스로 직접 labeling을 진행한다. 마우스로 드래그 한 영역이 history로 저장되고, xml파일이 생성된다.    
3) history를 사용하여, 그 다음 frame을 대상으로 template matching을 적용하여 매칭되는 부분을 찾는다.  
4) 대상 frame의 xml파일이 생성되며, 매칭된 영역이 자동으로 labeling 되고, history로 갱신된다.  
5) 3,4단계를 마지막 frame까지 반복 수행한다.  

## 4. auto_labeling_v1.py  동작 결과 (페트병 예시)

### AUTO_labeling_project/xml_files/xml_files.zip : 페트병 xml 압축 파일
### AUTO_labeling_project/xml_files/cup_xml_files.zip : 머그컵 xml 압축 파일

1) 첫 frame은 사용자가 직접 labeling 후 'w'키 입력  
![스크린샷, 2020-01-15 06-00-59](https://user-images.githubusercontent.com/46870741/72382463-a8660a80-375c-11ea-8dea-6e15dfe98d5c.png)


2) AUTO labeling
<img width="271" alt="스크린샷, 2020-01-15 05-58-29" src="https://user-images.githubusercontent.com/46870741/72382462-a8660a80-375c-11ea-8333-29e021d8f0ac.png">

3) test video

[![youtube영상](![img000001](https://user-images.githubusercontent.com/46870741/72382711-393ce600-375d-11ea-8845-56a1f123f107.jpg)](https://www.youtube.com/watch?v=M7Mv7iFjq6Q&feature=youtu.be)
