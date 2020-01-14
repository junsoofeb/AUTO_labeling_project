## 1. 개요

기존의 labeling 프로그램을 python으로 구현 (hand_labeling.py) 


## 2. 구현 환경

1) ubuntu 18.04
2) Python 3.6
3) OpenCV-python 4.2.0
4) Numpy 1.17

## 3. hand_labeling.py  동작 과정
### 시간관계상 모든이미지가 아닌 샘플 이미지를 뽑아서 수행했다.

1) 사용자가 label, 이미지파일이 들어있는 폴더의 경로, xml파일이 저장될 경로 등을 지정한다.  
2) 전체 이미지 중에서 랜덤으로 샘플을 선택한다. 첫 이미지는 항상 샘플에 포함된다.  
3) 샘플 이미지에 마우스로 labeling을 진행한다. 마우스 드래그 후 'w'를 누르면 끝.
4) 마우스 이벤트 좌표, 파일 이름, 폴더 경로 등 필요한 정보들을 이용해서 \*.xml파일을 생성한다.  

## 4. hand_labeling.py  동작 결과

1) labeling을 진행  
![h1](https://user-images.githubusercontent.com/46870741/72366640-00414900-373e-11ea-9ef4-fdec73af2ed7.png)

2) labeling을 진행 ( 마우스 드래그 )  
![h2](https://user-images.githubusercontent.com/46870741/72366642-00414900-373e-11ea-90b8-5cc335715330.png)

3) 결과는 <https://github.com/junsoofeb/AUTO_labeling_project/tree/master/Hand_labeling_implementation/xml_file>  
<img width="392" alt="h3" src="https://user-images.githubusercontent.com/46870741/72366643-00d9df80-373e-11ea-9b12-1e98d5f3d63c.png">
