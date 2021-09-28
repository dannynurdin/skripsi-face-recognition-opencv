import cv2
import numpy as np
import csv
import os
import logging

logging.basicConfig(filename='predict.log', format='%(asctime)s %(levelname)-8s %(message)s',level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

# global recognizer = cv2.face.LBPHFaceRecognizer_create()
# recognizer.read('train.yml')
# global faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# global font = cv2.FONT_HERSHEY_SIMPLEX

class Predict():
    def __init__(self, image):
        self.image = image
        # self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        # self.recognizer.read('train.yml')
        # self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # self.font = cv2.FONT_HERSHEY_SIMPLEX

    def print(self):
        return os.path.join('dataset', self.image)

    def predict(self):
        logging.info('-----------------------------')
        logging.info('Predict Start')
        # print(self.image)
        # print(os.path.join('dataset', self.image))
        # print('{} '.format(self.image))

        # logging.info('{}'.format(os.path.join('dataset', self.image)))
        # logging.info('{}'.format('dataset/{} '.format(self.image)))
        
        # img = cv2.imread('image/59b53e2d-0c03-44ec-a4a9-23d496caf6e0.jpg')
        img = cv2.imread(str(self.image))
        # img = cv2.imread(os.path.join('dataset', self.image)+ " ")

        
        
        

        logging.info('Recognizer start')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('model.yml')
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        font = cv2.FONT_HERSHEY_SIMPLEX
        ID = None
        CONF = None

        # recognizer = cv2.face.LBPHFaceRecognizer_create()
        # recognizer.read('train.yml')
        # faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # font = cv2.FONT_HERSHEY_SIMPLEX


        # img = cv2.imread('/home/ubuntu/skripsi/dataset/User.3.0.jpg ')
        # img = cv2.imread(self.image)

        ### resize image
        imgs = cv2.resize(img,(0,0),None,0.25,0.25)

        # convert to gray scale
        gray = cv2.cvtColor(imgs, cv2.COLOR_BGR2GRAY)

        ### detect the face
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=4,minSize=(30, 30))
        treshold = cv2.face_LBPHFaceRecognizer.getThreshold
        print(treshold)

        for (x,y,w,h) in faces:
            Id,conf = recognizer.predict(gray[y:y+h,x:x+w])
            # cv2.rectangle(imgS, (x,y), (x+w, y+h), (255,0,0), 2)
            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 260, 0), 2)
            # cv2.putText(imgS, str(Id), (x,y-40),font, 2, (255,255,255), 3)
            print('ID {0}, confidence {1}'.format(Id, conf))
            ID = Id
            CONF = conf
        logging.info('Predict result: {} with {} distance'.format(ID, CONF))
        print('ID {0}, confidence {1}'.format(ID, CONF))
        return ID,CONF
            
# # if __name__ = '__main__':
# #     pred = Predict()





# img = cv2.imread('/home/ubuntu/skripsi/dataset/User.3.0.jpg ')
# print(img)
# if img is None:
#     print('Wrong path:')
# # with open('imfile.txt', 'w') as f:
# #     for index in img:
# #         f.writelines('\n')
# #         for value in index:
# #             f.writelines(str(value))

# ### resize image
# imgS = cv2.resize(img,(0,0),None,0.25,0.25)


# # convert to gray scale
# gray = cv2.cvtColor(imgS, cv2.COLOR_BGR2GRAY)

# ### detect the face
# faces = faceCascade.detectMultiScale(gray, 1.1, 4)
# treshold = cv2.face_LBPHFaceRecognizer.getThreshold
# print(treshold)

# ### draw rectangle

# for (x,y,w,h) in faces:
#     Id,conf = recognizer.predict(gray[y:y+h,x:x+w])
#     cv2.rectangle(imgS, (x,y), (x+w, y+h), (255,0,0), 2)
#     # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 260, 0), 2)
#     cv2.putText(imgS, str(Id), (x,y-40),font, 2, (255,255,255), 3)
#     print('ID {0}, confidence {1}'.format(Id, conf))
    
# # cv2.imshow('im',imgS)
# # cv2.waitKey(0)
