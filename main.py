import os
import numpy as np
import secrets
from PIL import Image
from feature_extractor import FeatureExtractor
import glob
from flask import render_template, url_for, flash, redirect, request
import pickle
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from __init__ import db, bcrypt, app
from models import User
from forms import  RegistrationForm, LoginForm

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in glob.glob("static/feature/*"):
    features.append(pickle.load(open(feature_path, 'rb')))
    # print(feature_path)
    print('static/img/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')
    img_paths.append('static/img/' + os.path.splitext(os.path.basename(feature_path))[0] + '.jpg')


@app.route('/',  methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img']

        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat() + "_" + file.filename
        img.save(uploaded_img_path)
        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)  
        ids = np.argsort(dists)[:15] # Top 30 results
        scores = []
        for id in ids:
            if dists[id] >= 1.0 and dists[id] < 1.2 :
                scores.append((dists[id], img_paths[id]))

        print(scores)
        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run("0.0.0.0")
