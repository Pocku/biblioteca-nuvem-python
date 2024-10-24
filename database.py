import firebase_admin
import configparser

from firebase_admin import firestore
from firebase_admin import credentials

from globals import BookStatus
from globals import DATE_FORMAT
from datetime import datetime, timedelta

def read_config(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

userdata = read_config('assets/userdata.ini')
cred = credentials.Certificate("assets/privatekey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
collection_id = userdata['Collection']['id'] + userdata['Collection']['password']
stream = db.collection(collection_id).stream()

books = []
for doc in stream:
    dict = {
        "id": doc.id,
        "data": doc.to_dict()
    }
    books.append(dict)

def update():
    global books
    books = []
    stream = db.collection(collection_id).stream()
    for doc in stream:
        dict = {
            "id": doc.id,
            "data": doc.to_dict()
        }
        books.append(dict)
    print("Database realizou um update ao puxar dados mais recentes")
   

def add_book(data):
    doc = db.collection(collection_id).document()
    doc.set(data)
    print(f"Livro adicionado a biblioteca: {doc.id}")
    update()
    return doc.id

def get_book(unique_id):
    doc = db.collection(collection_id).document(unique_id)
    data = doc.get()
    return data.to_dict()

def edit_book(unique_id, new_data):
    doc = db.collection(collection_id).document(unique_id)
    doc.set(new_data)
    update()
    print(f'Livro {doc.id}: teve seu contéudo modificado!')
    return doc.id

def get_pendent_books():
    pendent = []

    for book in books:
        data = book['data']

        if data['usuario']:
            current_date = datetime.now()
            deadline_date = datetime.strptime(data['usuario']['dia_prazo'], DATE_FORMAT)

            if current_date > deadline_date:
                pendent.append(book)

    return pendent

def get_borrowed_books():
    array = []

    for book in books:
        if book['data']['status'] == BookStatus.EMPRESTADO:
            array.append(book)

    return array

def get_books_total():
    return len(get_realtime_books_in_collection())

def delete_book(unique_id):
    doc = db.collection(collection_id).document(unique_id)
    doc.delete()
    update()
    print(f'Livro deletado: {unique_id}')

def get_latest_books_in_collection():
    return books

def get_realtime_books_in_collection():
    stream = db.collection(collection_id).stream()
    array = []
    for doc in stream:
        dict = {
            "id": doc.id,
            "data": doc.to_dict()
        }
        array.append(dict)
    return array
    