from predict import Predict
from file_downloader import downloader, putData, getData
import recognize as re
import uuid
import os
import cv2
from tabulate import tabulate
import csv

class Pre():
    def __init__(self, image):
        self.img = image

    def start(self):
        # image_path = 'testing/image/{}.jpg'.format(uuid.uuid4())
        
        # # download video from s3
        # downloader_client = downloader(key=self.img,bucket='dannynurdin', destination=image_path)
        # downloader_client.download()

        model = Predict(self.img)
        sim = 0
        id,c = model.predict()
        # print('{}-{}'.format(id,c))
        if c:
            disMax = 140.0
            
            sim = 100-100/disMax*c
            # print('Similarity: ', sim)

        return id,c,sim

class Tra():
    def __init__(self, video):
        self.vid = video

    def start(self):
         # config
        face_cascade = 'lib/haarcascade_frontalface_default.xml'
        dataset_name = 'dataset/'
        samples = 10
        file_name = 'train.yml'
        video_path = 'video/testing-{}.mp4'.format(uuid.uuid4())

        # LBPH variables
        radius = 1
        neighbour = 8
        grid_x = 8
        grid_y = 8
        treshold = 140
        var = list([radius,neighbour,grid_x,grid_y,treshold])

        # download video from s3
        downloader_client = downloader(key=self.vid,bucket='skripsi200053-dev', destination=video_path)
        downloader_client.download()

        # start recognize using opencv
        model = Train(face_cascade,var,username)
        video = cv2.VideoCapture(video_path)
        model.createDataset(samples,video,dataset_name)
        id = model.train(dataset_name,file_name)

        print(id)

class testPutData():
    def run(self):
        test = putData('rodet','face006','99','heress')
        test.put()

class getImread():
    def __init__(self, path):
        self.path = path

    def run(self):
        img = cv2.imread(self.path)
        gray = img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        height, width = img_gray.shape

        print(f'{height}-{width}')
        print(gray[0][:9])
        print(gray[1][:9])
        print(gray[2][:9])
        print(gray[3][:9])
        print(gray[4][:9])
        print(gray[5][:9])

class getFilepath():
    def __init__(self, mypath):
        self.path = mypath

    def run(self):
        # onlyfiles = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        filepath = []
        for path in os.listdir(self.path):
            full_path = os.path.join(self.path, path)
            if os.path.isfile(full_path):
                filepath.append(full_path)
        return filepath

if __name__ == '__main__':
    # #
    # # predict image
    # #
    # p = Pre('/home/ubuntu/skripsi/testing_bab4/User.3.14.jpg ')
    # p.start()
    # t = Tra('')

    # #
    # # train model
    # #
    # faces,faceID = re.labels_for_training_data('testing_bab4/dataset')
    # face_recognizer=re.train_classifier(faces,faceID)
    # face_recognizer.save(f'{os.path.dirname(os.path.realpath(__file__))}/testing_bab4_model.yml')
    # print(f'faces: {len(faces)} , id: {len(faceID)}')


    # test = testPutData()
    # test.run()
    # test = putData('rodet','face006','9976','heress')
    # test.put()

    #
    # get imread
    #
    # imRead = getImread('/home/ubuntu/skripsi/dataset/User.3.0.jpg ')
    # imRead.run()

    # #
    # # get all filepath
    # #
    # filepath = getFilepath('/home/ubuntu/skripsi/testing_bab4/test/3')
    # onlyfiles = [f for f in os.listdir('/home/ubuntu/skripsi/testing_bab4/test/3') if os.path.isfile(os.path.join('/home/ubuntu/skripsi/testing_bab4/test/3', f))]
    # data = filepath.run()
    # table_data = []
    # head = ['No', 'Actual', 'Predict', 'Confidence', "Similarity"]

    # for index,file in enumerate(data):
    #     print('===================================')
    #     print(f'{index}. {file}')
    #     p = Pre(file)
    #     id,c,sim = p.start()
    #     table_data.append([index,onlyfiles[index],id,c,sim])
    #     print('===================================')
    
    # print(tabulate(table_data, headers=head, tablefmt="grid"))
    # with open('result.csv', 'w') as f:
    #     write = csv.writer(f)
    #     write.writerow(head)
    #     for data in table_data:
    #         write.writerow(data)

    ## Get Data from dynamoDB
    # ids = "dc538654-c341-4a80-9a80-e8849c00b57a"
    # dynamodb_client = getData(ids)
    # response = dynamodb_client.get()
    # print(type(response))
    # print(response['Item']['name']['S'])
    
    
    expect_username = 'd771d2ce-ba2a-4f32-a156-f28264cab1af'
    ids = 1
    conf = 65
    location = 'wanayasa'

    dynamodb_client = getData(id = expect_username)
    dynamodb_response = dynamodb_client.get()
    # print(dynamodb_response)
    print(dynamodb_response['Item']['name']['S'])

    record = putData(id =expect_username, name = dynamodb_response['Item']['name']['S'],face_id=ids,conf=conf,location=location)
    rrr = record.put()
    print(rrr)
    

    
    



