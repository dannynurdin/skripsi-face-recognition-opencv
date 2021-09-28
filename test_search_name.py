# username = None
# with open('users.txt') as f:
#     datafile = f.readlines()
#     for line in datafile:
#         id = line.split(',')[0]
#         if id == '121':
#             print(line.split(',')[1])
#             username = line.split(',')[1]

# print(username)

# data = '17,kamaludinss'

# li = data.split(',')[0]
# print(li)
# import json

# class updateData():
#     def print(self, data):
        
#         print(json.dumps(data, sort_keys=True, indent=4))
#     def update(self):
#         response = dynamodb.update_item(
#             ExpressionAttributeNames={
#                 '#V': 'video',
#             },
#             ExpressionAttributeValues={
#                 ':v': {
#                     'S': self.key,
#                 }
#             },
#             Key={
#                 'id': {
#                     'S': self.id,
#                 }
#             },
#             ReturnValues='ALL_NEW',
#             TableName='faceApp-UserPool',
#             UpdateExpression='SET #V = :v',
#         )
#         # faceApp-UserPool
#         return response


# if __name__ == '__main__':
#     update = updateData()

#     datas = {
#         "#V": "video123",
#         "#s": "video1",
        
#     }

#     print(datas)
#     datas['#W'] = { 'S' : 'apaansin'}
#     print(datas)
from file_downloader import SearchUser, getData

target = '4'
hasil = None

with open('users.txt') as f:
    datafile = f.readlines()
    for data in datafile:
        id = data.split(',')
        if  target == id[0]:
            hasil = id[1]
        else:
            hasil = 'salah'
print(hasil)
test = SearchUser(1)
user = test.search()

print('User: ',user)
print('User Len: ',len(user))
user_new = user.replace("\n","")
print('User New: ', user_new)
print('User New Len: ',len(user_new))
print('User Len -f: ',len('d771d2ce-ba2a-4f32-a156-f28264cab1af'))

dynamodb_client = getData(id = str(user.replace("\n","")))
res = dynamodb_client.get()
print(res['Item'])