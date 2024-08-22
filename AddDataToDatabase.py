import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://criminafacedetection-default-rtdb.firebaseio.com/'
})

ref = db.reference('Criminals')


data = {
    "1234":
        {
            "name" : "Tejas Garg",
            "crime" : "Cybercrime",
            "DOB" : "5/11/2002",
            "religion" : "Hindu"
        },
    "1235":
        {
            "name" : "Harsh Gupta",
            "crime" : "Delhi Riots",
            "DOB" : "25/11/2003",
            "religion" : "Muslim"
        },
    "1236":
        {
            "name" : "Rupansh Kumar",
            "crime" : "Murder",
            "DOB" : "21/02/2003",
            "religion" : "Afgani"
        },       
    "1237":
        {
            "name" : "Shikshit",
            "crime" : "Trafficking",
            "DOB"  : "05/02/2003",
            "religion" : "muslim"
        }
}

for key,value in data.items():
    ref.child(key).set(value)