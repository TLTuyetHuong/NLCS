#========================================================
# dataSetCreator
import cv2
import numpy
import sqlite3
import os

# Insert or update vao Sqlite
def insertOrUpdate(id, ten, tuoi, gioitinh):
    conn = sqlite3.connect('data.db')
    query = "Select * from People where id= "+ str(id)
    cursor = conn.execute(query)
    isRecordExist = 0
    for row in cursor:
        isRecordExist = 1
    if(isRecordExist == 0):
        query = "Insert into People(id, ten, tuoi, gioitinh) values("+str(id)+",'"+str(ten)+"','"+str(tuoi)+"','"+str(gioitinh)+"')"
    else:
        query = "Update People set ten = '"+str(ten)+"', tuoi= '"+str(tuoi)+"', gioitinh= '"+str(gioitinh)+"' Where id= "+str(id)

    conn.execute(query)
    conn.commit()
    conn.close()

# Insert vao db
id = input("Nhap vao id: ")
ten = input("Nhap vao ten: ")
tuoi = input("Nhap vao tuoi: ")
gioitinh = input("Nhap vao gioi tinh: ")
insertOrUpdate(id, ten, tuoi, gioitinh)

# Load tv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+ "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
sampNum = 0

while(True):
    # camera ghi hinh
    ret, fram = cap.read()
    gray= cv2.cvtColor(fram, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in faces:
        cv2.rectangle(fram, (x,y), (x+w, y+h), (0,255,0), 2)
    if not os.path.exists('dataSet'):
        os.makedirs('dataSet')
    # So anh lay tang dan
    sampNum += 1
    # Luu anh da chup khuon mat vao file du lieu
    cv2.imwrite('dataSet/User.'+str(id)+'.'+str(sampNum)+'.jpg', gray[y:y+h,x:x+w])
    cv2.imshow('fram', fram)
    cv2.waitKey(1)

    # Thoat ra neu so luong anh nhieu hon 50
    if sampNum > 50:
        break
cap.release()
cv2.destroyAllWindows()

#===========================================================
# Trainning
import cv2,os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path='dataSet'

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        #split to get ID of the image
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        print (ID)
        IDs.append(ID)
        cv2.imshow("traning",faceNp)
        cv2.waitKey(10)
    return IDs, faces

Ids,faces=getImagesAndLabels(path)
#trainning
recognizer.train(faces,np.array(Ids))
if not os.path.exists('recognizer'):
    os.makedirs('recognizer')

recognizer.save('recognizer/trainningData.yml')
cv2.destroyAllWindows()

#=========================================================
# detector
import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
cam = cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/trainningData.yml")
id = 0
# set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (203, 23, 252)


# get data from sqlite by ID
def getProfile(id):
    conn = sqlite3.connect("data.db")
    cmd = "SELECT * FROM People WHERE id=" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


while (True):
    # camera read
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        id, conf = rec.predict(gray[y:y + h, x:x + w])
        profile = getProfile(id)
        # set text to window
        if (profile != None):
            # cv2.PutText(cv2.fromarray(img),str(id),(x+y+h),font,(0,0,255),2);
            cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 30), fontface, fontscale, fontcolor, 2)
            cv2.putText(img, "Age: " + str(profile[2]), (x, y + h + 60), fontface, fontscale, fontcolor, 2)
            cv2.putText(img, "Gender: " + str(profile[3]), (x, y + h + 90), fontface, fontscale, fontcolor, 2)

        cv2.imshow('Face', img)
    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
