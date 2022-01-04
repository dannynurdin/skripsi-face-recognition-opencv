import boto3
import datetime
import logging

logging.basicConfig(filename='testing.log', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

s3 = boto3.client('s3',aws_access_key_id='AKIA5O74KBBP4GOP6BE3',aws_secret_access_key='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')
dynamodb= boto3.client('dynamodb',aws_access_key_id='AKIA5O74KBBP4GOP6BE3',aws_secret_access_key='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', region_name='ap-southeast-1')

class downloader():

    def __init__(self, key, bucket, destination):
        self.Key = key
        self.Bucket = bucket
        self.Destination = destination

    def download(self):
        print(self.Key)
        print(self.Bucket)
        print(self.Destination)
        s3.download_file(self.Bucket, self.Key, self.Destination)

class getData():
    def __init__(self, id):
        self.key = str(id)
    
    def get(self):
        response = dynamodb.get_item(
            TableName = "faceApp-UserPool",
            Key= {
                "id": {"S": self.key}
            }
        )
        return response

class updateData():
    def __init__(self, ids, key):
        self.id = str(ids)
        self.key = str(key)

    def update(self):
        response = dynamodb.update_item(
            ExpressionAttributeNames={
                '#V': 'video',
            },
            ExpressionAttributeValues={
                ':v': {
                    'S': self.key,
                }
            },
            Key={
                'id': {
                    'S': self.id,
                }
            },
            ReturnValues='ALL_NEW',
            TableName='faceApp-UserPool',
            UpdateExpression='SET #V = :v',
        )
        # faceApp-UserPool
        return response

class updateDataNew():
    def __init__(self,key):
        self.key = str(key)

    def update(self, AttrName, AttrValue, Expression):
        response = dynamodb.update_item(
            ExpressionAttributeNames=AttrName,
            ExpressionAttributeValues=AttrValue,
            Key={
                'id': {
                    'S': self.key,
                }
            },
            ReturnValues='ALL_NEW',
            TableName='faceApp-UserPool',
            UpdateExpression=Expression,
        )
        return response

class putData():
    def __init__(self, id, name, face_id, conf, location):
        self.year = str(datetime.datetime.now().year)
        self.time = datetime.datetime.today()
        self.user_id = str(id)
        self.name = str(name)
        self.face_id = str(face_id)
        self.confidence = str(conf)
        self.location = str(location)

    def put(self):
        # try:
        print('MULAI')
        logging.info('STATUS => mulai')
        logging.info('PARAMS => year: ', self.year)
        logging.info('PARAMS => time: ', self.time)
        logging.info('PARAMS => user_id: ', self.user_id)
        logging.info('PARAMS => Name: ', self.name)
        logging.info('PARAMS => face_id: ', self.face_id)
        logging.info('PARAMS => confidence: ', self.confidence)
        logging.info('PARAMS => location: ', self.location)

        today = datetime.datetime.today() + datetime.timedelta(hours=7)
        times = today.strftime('%Y-%m-%d,%H:%M:%S')

        status = 'Self Attendance'
        timeLimit = 8

        if today.hour >= timeLimit:
            status = "Late"

        response = dynamodb.put_item(
            TableName = 'test-v2',
            Item = {
                "type": {
                    "S": self.year
                },
                "date": {
                    "S": str(times)
                },
                "location": {
                    "S": self.location
                },
                "confidence": {
                    "S": self.confidence
                },
                "face_id": {
                    "S": self.face_id
                },
                "tgl": {
                    "S": times.split(',')[0]
                },
                "time": {
                    "S": times.split(',')[1]
                },
                "group": {
                    "S": "employee"
                },
                "id": {
                    "S": self.user_id
                },
                "name": {
                    "S": self.name
                },
                "status": {
                    "S": status
                }
            },
        )
        print('SELESAI : ', response)
        
        logging.info('STATUS => selesai: ', response)
        return response
        # except Exception as e:
        #     print('ERROR on =>', e)
        #     logging.info('ERROR => ',e)

class SearchUser():
    def __init__(self, id):
        self.id = id

    def search(self):
        
        print('id: ',self.id)
        with open('users.txt') as f:
            datafile = f.readlines()
            for data in datafile:
                dataLine = data.split(',')
                if str(dataLine[0]) == str(self.id):
                    print('DataLine: ',dataLine)
                    print('DataLine[1]: ',dataLine[1])
                    return dataLine[1]
