import os
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
import glob
import flask_login as fl
import pickle
from datetime import datetime
from flask import Flask, request, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in glob.glob("static/feature/*"):
    features.append(pickle.load(open(feature_path, 'rb')))
    # print(feature_path)
    # print('static/img/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')
    img_paths.append('static/img/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')


db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    return render_template("login.html")

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat() + "_" + file.filename
        img.save(uploaded_img_path)
        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)  # Do search
        ids = np.argsort(dists)[:10] # Top 30 results
        scores = []
        for id in ids:
            if dists[id] > 1.1 and dists[id] < 1.2 :
                scores.append((dists[id], img_paths[id]))

        print(scores)
        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run("0.0.0.0")
