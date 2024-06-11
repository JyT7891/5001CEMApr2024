import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("C:/Users/ASUS/PycharmProjects/SoftwareEngineering/cad_firebase.json")
firebase_admin.initialize_app(cred)
