import firebase_admin
from firebase_admin import credentials, firestore


#fetch the service account key JSON file content
def initializeFirebase():
    cred = credentials.Certificate('cad_firebase.json')
    firebase_admin.initialize_app(cred)


def getClient():
    return firestore.client()
