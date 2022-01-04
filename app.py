from flask import Flask, request, make_response
from flask_cors import CORS
from file_downloader import downloader, getData, updateData, updateDataNew, putData, SearchUser
import cv2
from train import Train
from predict import Predict
import uuid
import os
import datetime
import json
import logging
import math
import recognize as re

logging.basicConfig(filename='skripsi.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def test():
    current_time =  datetime.datetime.now()
    response = make_response('<h1>Success at test {} (server time)</h1>'.format(current_time))
    response.headers['Content-Security-Policy'] = 'upgrade-insecure-requests'
    return response

@app.route('/recognize/predict', methods=['POST'])
def predict():
    logging.info('halo')
    request_data = request.get_json()
    ids = None
    
    if request_data:
        image = request_data['image']
        expect_username = request_data['username']
        location = request_data['location']
        username = None
        conf = None
        TEST_DB = None
        

        debug_id = None
        debug_sim = None
        debug_dis = None
        debug_username = None

        result_id = None
        result_sim = None
        result_dis = None
        result_username = None

        debug_user_data = None
        result_user_data = None

        minSim = 40 # 75%
        
        image_path = 'image/{}.jpg'.format(uuid.uuid4())

        # download video from s3
        downloader_client = downloader(key=image,bucket='dannynurdin', destination=image_path)
        downloader_client.download()
        
        model = Predict(image_path)
        
        res = model.print()
        ids,c = model.predict()
        logging.info('DATA => id from model == ', ids)
        print('DATA => id from model == ', ids)
        logging.info('success {} - {}'.format(ids, c))
        if c:
            disMax = 140.0
            simMax = 100
            similarity  = simMax - simMax/disMax*c
            conf = similarity

        ## search user in Users.txt
        user = SearchUser(ids)
        userId = user.search()

        ## get user data from dynamodb
        dynamodb_client = getData(id = userId.replace("\n",""))
        dynamodb_response = dynamodb_client.get()

        # add record to database test-v2
        if expect_username == userId.replace("\n",""):
            dynamodb_client2 = getData(id = expect_username)
            dynamodb_response2 = dynamodb_client2.get()

            record = putData(id = expect_username, name = dynamodb_response2['Item']['name']['S'],face_id=ids,conf=conf,location=location)
            record.put()
            TEST_DB = 'success'

           
        
        # with open('users.txt') as f:
        #     datafile = f.readlines()
        #     for line in datafile:
        #         Id = line.split(',')
        #         print('DATA => Id from model == ', Id[0])
        #         logging.info('DATA => Id from model == ', Id[0])

        #         if Id[0] == id:
        #             dump= line.split(',')[1]
        #             debug_username = dump.split('\n')[0]
        #             debug_id = id
        #             debug_sim = conf
        #             debug_dis = c
                    
        #             dynamodb_client = getData(id = debug_username)
        #             debug_response = dynamodb_client.get()
        #             debug_user_data = debug_response['Item'] or None

        #             # add record to database test-v2
        #             record = putData(id = debug_username,face_id=debug_id,conf=debug_sim,location='test location')
        #             record.put()
                    
        #             if conf and conf >= minSim:
        #                 result_username = dump.split('\n')[0]
        #                 result_sim = conf
        #                 result_id = id
        #                 result_dis = c

        #                 dynamodb_client = getData(id = result_username)
        #                 result_response = dynamodb_client.get()
        #                 result_user_data = result_response['Item'] or None
        
        

        # response = make_response({
        #     "debug": {
        #         "id": id,
        #         "dis": debug_dis,
        #         'sim': debug_sim,
        #         "username": debug_username,
        #         "user_data": debug_user_data,
        #         'expect_user': expect_username

        #     },
        #     'result': {
        #         "username": result_username,
        #         "dis": result_dis,
        #         "sim": result_sim,
        #         "id": result_id,
        #         "user_data": result_user_data
        #     },
            
        # })

                
        response = {
            'id': ids,
            'user': dynamodb_response['Item'],
            'location': location,
            'db': TEST_DB,
            'user_id': userId.replace("\n",""),
            'expect_user': expect_username
        }
        # response.headers['Content-Security-Policy'] = 'upgrade-insecure-requests'
        return response
    
    return 'kosong'
    

        # if image is None:
        #     value = {
        #         statusCode : 400,
        #         message : 'Image required!',
        #     }
        #     return json.dumps(value)
        # model = Predict(image)
        # id, conf = model.predict()

        # response = {
        #     statusCode : 200,
        #     data : {
        #         id : id,
        #         conf : conf,
        #         status : success,
        #     }
        # }
        # return json.dumps(response)    

@app.route('/recognize/train', methods=['POST'])
def train():
    # grab data from post request
    request_data = request.get_json()

    key = None
    username = None

    # config
    face_cascade = 'lib/haarcascade_frontalface_default.xml'
    dataset_name = 'dataset/'
    samples = 15
    file_name = 'model.yml'
    video_path = 'video/{}.mp4'.format(uuid.uuid4())
    
    
    # LBPH variables
    radius = 1
    neighbour = 8
    grid_x = 8
    grid_y = 8
    treshold = 140
    var = list([radius,neighbour,grid_x,grid_y,treshold])

    if request_data:

        if 'key' in request_data:
            key = request_data['key']
        
        if 'username' in request_data:
            username = request_data['username']

        if 'from' in request_data:
            status = request_data['from']

        if status =='development':
            bucket_name = 'skripsi200053-dev'
        else:
            bucket_name =  'skripsi132739-prod'

        

        # download video from s3
        downloader_client = downloader(key=key,bucket=bucket_name, destination=video_path)
        downloader_client.download()

        # get data user
        dynamodb_client = updateData(id = username, key = key)
        ress = dynamodb_client.update()
        print(ress)

        # start recognize using opencv
        model = Train(face_cascade,var,username) # create instance train
        video = cv2.VideoCapture(video_path) # load video
        model.createDataset(samples,video,dataset_name) # create dataset
        # id = model.train(dataset_name,file_name)

        faces,faceID = re.labels_for_training_data('dataset')
        face_recognizer=re.train_classifier(faces,faceID)
        face_recognizer.save(f'{os.path.dirname(os.path.realpath(__file__))}/model.yml')
        print(f'faces: {len(faces)} , id: {len(faceID)}')

        response = {
            "success": True,
            "face_id": id,
            "username": username
        }

        response = make_response({
            "success": True,
            "face_id": id,
            "username": username            
        })
        response.headers['Content-Security-Policy'] = 'upgrade-insecure-requests'
        return response
    else:
        return 'Key required!'

@app.route('/update', methods=['POST'])
def update():
    request_data = request.get_json()
    AttrName = {}
    AttrValue = {}
    Expression = []
    ids = None

    if request_data:
        if 'id' in request_data:
            ids = request_data['id']
            

        if 'name' in request_data:
            # key = request_data['name']
            AttrName['#N'] = 'name'
            AttrValue[':N'] = { 'S' : request_data['name']}
            Expression.append('#N = :N')


        if 'phone' in request_data:
            # status = request_data['phone']
            AttrName['#P'] = 'phone_number'
            AttrValue[':P'] = { 'S' : request_data['phone']}
            Expression.append('#P = :P')

        if 'address' in request_data:
            # status = request_data['address']
            AttrName['#A'] = 'address'
            AttrValue[':A'] = { 'S' : request_data['address']}
            Expression.append('#A = :A')

    
    expression = 'Set ' + ','.join([str(elem) for elem in Expression])

    dynamodb_client = updateDataNew(ids)
    ress = dynamodb_client.update(AttrName,AttrValue, expression) 

    response = make_response({
            "res": request_data,
            'AttrName': json.dumps(AttrName),
            'AttrValue': json.dumps(AttrValue),
            'Expression': expression
            
        })
    response.headers['Content-Security-Policy'] = 'upgrade-insecure-requests'
    return response
if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(host='0.0.0.0.0',port=80)