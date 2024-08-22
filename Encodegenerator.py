import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://criminafacedetection-default-rtdb.firebaseio.com/',
    'storageBucket' : 'criminafacedetection.appspot.com'
})



# importing student images
FolderPath = 'Images'
PathList = os.listdir(FolderPath)
print(PathList)
imgList = []
StudentIds = []
for path in PathList:
    imgList.append(cv2.imread((os.path.join(FolderPath,path))))
    StudentIds.append(os.path.splitext(path)[0])
    # print(path)
    # print(os.path.splitext(path)[0])

    fileName = f'{FolderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)





print(StudentIds)

def findEncodings(imagesList):
    encodeList=[]
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started . . .")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown,StudentIds]
print("Encoding Complete") 

file=open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("File Saved")