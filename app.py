from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import certifi
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

connectionString = os.environ.get("MONGODB_URI")
databaseName = os.environ.get("DB_NAME")

certificate = certifi.where()
client = MongoClient(connectionString, tlsCAFile=certificate)

db = client[databaseName]

app = Flask(__name__) 

@app.route('/')
def home():
    return render_template('index.html')

# Routing untuk membuat API
@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    profile_name = f'profile-{mytime}.{extension}'
    save_to = f'static/{profile_name}'
    profile.save(save_to)


    # hasil akan menjadi: 2022-11-05-09-02-59
    timestamps = today.strftime('%Y.%m.%d | %H:%M:%S')
    # ubah menjadi: 2022.11.05 | 09:02:59


    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    doc = {
        'file': filename,
        'profile': profile_name,
        'title': title_receive,
        'content': content_receive,
        'time': timestamps,
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'data was saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)