# Image Repo

  

user login application that allows users to search images based on uploaded images.

Tensor flow Keras model used for image recognition and scoring.

  

### How To Run

1. Clone repo: **git clone https://github.com/musemen/ImageRepo.git**

2. **cd ImageRepo** and set up virtual environment
	* __virtualenv env__
	* __source env/bin/activate__
3. Install requirements
	* **pip install - requirements.txt**
4. Add images to the static/img directory and run the __offline.py__ script to train run  VGG16 model, with weights pre-trained on ImageNet. (more info [here](https://keras.io/applications/#vgg16 "Title"))
5. run project by running __main.py__. This will open a web UI on local host port 5000/
6. Login or create a new account (user information stored in SQLite DB)
7. Upload Images and get results for images that are similar.
