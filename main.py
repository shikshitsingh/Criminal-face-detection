import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://criminafacedetection-default-rtdb.firebaseio.com/',
    'storageBucket' : 'criminafacedetection.appspot.com'
})

bucket=storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground= cv2.imread('Resources/background 2.png')


# importing the mode images into a list
FolderModePath = 'Resources/Modes'
modePathList = os.listdir(FolderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread((os.path.join(FolderModePath,path))))
# print(len(imgModeList))


#load the encoding file

print("Loading Encode File . . .")
file=open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown,StudentIds = encodeListKnownWithIds
# print(StudentIds)
print("Encode File Loaded")

counter=0
id = -1
imgcriminal=[]
while(True):
    success , img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    FaceCurframe = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,FaceCurframe)


    img_resized = cv2.resize(img,(640,480))
    imgBackground[162:162+480 , 55:55+640]=img_resized
    imgBackground[44:44+633 , 808:808+414]=imgModeList[1]

    for encodeFace , faceloc in zip(encodeCurFrame,FaceCurframe):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        # print("matches",matches)
        # print("FaceDis",faceDis)

        matchIndex = np.argmin(faceDis)
        # print("Match Index",matchIndex)

        if matches[matchIndex]:
            # print("Known face detected")
            # print(StudentIds[matchIndex])
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            bbox = 55+x1,162+y1,x2-x1,y2-y1
            imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
            id = StudentIds[matchIndex]

            
        
            #get the data
            criminalInfo = db.reference(f'Criminals/{id}').get()
            print(criminalInfo)
            #get the image from storage
            blob= bucket.get_blob(f'Images/{id}.png')
            array=np.frombuffer(blob.download_as_string(),np.uint8)
            imgcriminal = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
        
            cv2.putText(imgBackground,str(criminalInfo['crime']),(1006,550),
                    cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
            cv2.putText(imgBackground,str(criminalInfo['DOB']),(1006,493),
                    cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)


            (w, h), _ =cv2.getTextSize(criminalInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
            offset = (440-w)//2    
            cv2.putText(imgBackground,str(criminalInfo['name']),(808+offset,445),
                    cv2.FONT_HERSHEY_COMPLEX,1,(50,50,50),1)  

        imgresized1 = cv2.resize(imgcriminal,(216,216))
        imgBackground[175:175+216,909:909+216]=imgresized1

        

    cv2.imshow("Criminal Face Detection System",imgBackground)
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cap.release()
cv2.destroyAllWindows()   