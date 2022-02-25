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

