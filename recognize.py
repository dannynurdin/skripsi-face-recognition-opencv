
import numpy as np
import cv2
import os


#Face detection is done
def faceDetection(test_img):             
    gray_img=cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    face_haar=cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
    faces=face_haar.detectMultiScale(gray_img, scaleFactor=1.2,
        minNeighbors=4,     
        minSize=(30, 30))
    return faces,gray_img

# labeling dataset
def labels_for_training_data(directory):
    faces=[]
    faceID=[]
    file_count = 0


    for path,subdirnames,filenames in os.walk(directory):
        for filename in filenames:
            if filename.startswith("."):
                print("skipping system file")
                continue
            file_count += 1
            print(f'{filename} with id: {filename.split(".")[1]}')
            id = filename.split(".")[1]

            image = cv2.imread(f'dataset/{filename}')
            if image is None:
                print(f'{filename} not exist!')
                continue

            faces_rect,gray_img=faceDetection(image)
            if len(faces_rect)!=1:
                print(f'{filename} -> no/multiple face detected')
                
                continue

            (x,y,w,h)=faces_rect[0]
            tiny_face=gray_img[y:y+w,x:x+h]

            faces.append(tiny_face)
            
            faceID.append(int(id))

    print(f'{file_count=}')
    return faces,faceID

#Here training Classifier is called
def train_classifier(faces,faceID):                              
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces,np.array(faceID))
    face_recognizer.write(f'{os.path.dirname(os.path.realpath(__file__))}/model.yml')
    return face_recognizer


#Drawing a Rectangle on the Face Function
def draw_rect(test_img,face):                                      
    (x,y,w,h)=face
    cv2.rectangle(test_img,(x,y),(x+w,y+h),(0,255,0),thickness=3)

#Putting text on images
def put_text(test_img,text,x,y):                                    
    cv2.putText(test_img,text,(x,y),cv2.FONT_HERSHEY_DUPLEX,3,(255,0,0),6)

