import boto3
import datetime

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
        self.key = id
    
    def get(self):
        response = dynamodb.get_item(
            TableName = "faceApp-UserPool",
            Key= {
                "id": {"S": self.key}
            }
        )
        return response

class updateData():
    def __init__(self, id, key):
        self.id = id
        self.key = key

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
        self.key = key

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
    def __init__(self, id, face_id, conf, location):
        self.year = str(datetime.datetime.now().year)
        self.time = str(datetime.datetime.today().strftime('%Y-%m-%d,%H:%M:%S'))
        self.user_id = id
        self.face_id = face_id
        self.confidence = conf
        self.location = location

    def put(self):
        try:
            print('MULAI')
            dynamodb.put_item(
                TableName = 'test-v2',
                Item = {
                    "type": {
                        "S": self.year
                    },
                    "date": {
                        "S": self.time
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
                        "S": self.time.split(',')[0]
                    },
                    "time": {
                        "S": self.time.split(',')[1]
                    },
                    "group": {
                        "S": "employee"
                    },
                    "name": {
                        "S": self.user_id
                    }
                },
            )
            print('SELESAI')
        except Exception as e:
            print('ERROR on =>', e)

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
