import cv2
import os
import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import argparse as arg


class Train():
    
    def __init__(self, face_cascade,config,username):
        self.username = username
        # self.current_dir = current_dir
        self._Face_Cascade = cv2.CascadeClassifier(face_cascade)
        self.dataset_path("dataset/")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create(config[0], config[1], config[2], config[3],config[4])

    def dataset_path(self, path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)

    def ReadName(self):
        NAME = []
        with open ("users.txt", "r") as f:
            for line in f:
                NAME.append(line.split(",")[1].rstrip())
        return NAME

    def AddUser(self):
        # Name = input('\n[INFO] Masukan nama user : ')
        Name = self.username
        info = open('users.txt', "a+")
        ID = len(open("users.txt").readlines(  ))
        info.write(str(ID) + "," + Name + "\n")
        print("\n[INFO] Tambah user berhasil, ID:" + str(ID))
        info.close
        return ID

    def getImageWithLabels(self,path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            img = cv2.imread(imagePath, 0)
            img_numpy = np.array(img, 'uint8')
            id = int(os.path.split(imagePath)[- 1].split('.')[1])
            faceSamples.append(img_numpy)
            ids.append(id)
        return faceSamples, ids

    def train(self, path, file_name):
        # os.chdir('tmp')
        # real_path = '{0}/{1}'.format(self.current_dir,path)
        print("\n[INFO] Training wajah sedang dimulai...")
        time.sleep(1)
        faces, ids = self.getImageWithLabels(path)
        self.recognizer.update(faces,np.array(ids))
        self.recognizer.write(file_name)
        print("\n[INFO] Model sukses melatih  user ID: {0}".format(len (np.unique (ids))))
        print("\n[INFO] Menutup program")
        return len(np.unique (ids))

    def create_Rect(self, Image, face, color):
        x,y,w,h = face
        cv2.line(Image, (x, y), (int(x + (w/5)),y), color, 2)
        cv2.line(Image, (int(x+((w/5)*4)), y), (x+w, y), color, 2)
        cv2.line(Image, (x, y), (x,int(y+(h/5))), color, 2)
        cv2.line(Image, (x+w, y), (x+w, int(y+(h/5))), color, 2)
        cv2.line(Image, (x, int(y+(h/5*4))), (x, y+h), color, 2)
        cv2.line(Image, (x, int(y+h)), (x + int(w/5) ,y+h), color, 2)
        cv2.line(Image, (x+int((w/5)*4), y+h), (x + w, y + h), color, 2)
        cv2.line(Image, (x+w, int(y+(h/5*4))), (x+w, y+h), color, 2)
        
    def createDataset(self,samples,cam,dataset_name):
        fig, axs = plt.subplots(10,5,figsize=(20,20), facecolor='w', edgecolor='k')
        fig.subplots_adjust(hspace=.5, wspace=.001)
        self.dataset_path(dataset_name)
        count = 0
        face_id = self.AddUser()
        print('\n[INFO] Membuat dataset')
        while(True):
            success, image = cam.read()
            # convert image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self._Face_Cascade.detectMultiScale(gray, scaleFactor = 1.098, minNeighbors = 6, minSize = (50, 50))
            if(len(faces)> 1):
                print('\n[WARNING] Terdeteksi lebih dari 1 wajah')
                continue
            try:
                for _,face in enumerate(faces):
                    x, y, w, h = face
                    gray_chunk = gray[y-30: y + h + 30, x-30: x + w + 30]
                    image_chunk = image[y: y + h, x: x + w]
                    self.create_Rect(image, face, [0,255,0])
                    # cv2.imshow("Video", image)
                    #get center image
                    # image_center = tuple(np.array(gray_chunk.shape) / 2)
                    # rot_mat = cv2.getRotationMatrix2D(image_center, angle_degree, 1.0)
                    # rotated_image = cv2.warpAffine(gray_chunk, rot_mat, gray_chunk.shape, flags=cv2.INTER_LINEAR)
                    print("\n[INFO] Adding image number {} to the dataset".format(count))
                    # Save image
                    cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg " ,
                        image)
                    axs[int(count/5)][count%5].imshow(image,cmap='gray', vmin=0, vmax=255)
                    axs[int(count/5)][count%5].set_title("Person." + str(face_id) + '.' + str(count) + ".jpg ", 
                        fontdict={'fontsize': 15,'fontweight': 'medium'})
                    axs[int(count/5)][count%5].axis('off')
                    count += 1
            except Exception as e:
                print(e)
                print('[WARNING] Ada error')
                continue
            if cv2.waitKey(1) & 0xff == 27:
                break
            elif count >= samples:
                break
        print('\n[INFO] Dataset berhasil dibuat')
        # cam.release()
        # cv2.destroyAllWindows()
        # plt.show()
def Arg_Parse():
	Arg_Par = arg.ArgumentParser()
	Arg_Par.add_argument("-v", "--video",
					help = "path of the video or if not then webcam")
	Arg_Par.add_argument("-c", "--camera",
					help = "Id of the camera")
	arg_list = vars(Arg_Par.parse_args())
	return arg_list

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Masukan argumen yang valid!")
        sys.exit()
    Arg_list = Arg_Parse()
    face_cascade = 'lib/haarcascade_frontalface_default.xml'
    if not (os.path.isfile(face_cascade)):
        raise RuntimeError("%s: not found" % face_cascade)
    samples = 2
    dataset_name = 'dataset/'
    file_name = 'train.yml'
    radius = 1
    neighbour = 8
    grid_x = 8
    grid_y = 8
    treshold = 140
    var = list([radius,neighbour,grid_x,grid_y,treshold])
    model = Train(face_cascade,var)
    if Arg_list["video"] != None :
        video = cv2.VideoCapture(Arg_list["video"])
        #create a dataset for further model training
        print('{0} {1} {2}'.format(samples,video,dataset_name))
        model.createDataset(samples,video,dataset_name)
        #Training the model
        model.train(dataset_name,file_name)
    if Arg_list["camera"] != None :
        camera = cv2.VideoCapture(eval(Arg_list["camera"]))
        camera.set(3, 640)
        camera.set(4, 480)
        model.createDataset(samples,camera,dataset_name)
        #Training the model
        model.train(dataset_name,file_name)