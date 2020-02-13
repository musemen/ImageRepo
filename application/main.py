import os
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
import glob
import flask_login as fl
import pickle
from datetime import datetime
from flask import Flask, request, render_template, Blueprint
from __init__ import app

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in glob.glob("application/static/feature/*"):
    features.append(pickle.load(open(feature_path, 'rb')))
    img_paths.append('application/static/img/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')

main = Blueprint('main', __name__)

# @app.route('/')
# def index():
#     return 'Index'


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    fl.logout_user()
    return redirect(url_for('main.index'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "application/static/uploaded/" + datetime.now().isoformat() + "_" + file.filename
        img.save(uploaded_img_path)

        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)  # Do search
        ids = np.argsort(dists)[:30] # Top 30 results
        scores = [(dists[id], img_paths[id]) for id in ids]

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run("0.0.0.0")
