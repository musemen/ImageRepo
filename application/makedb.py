from __init__ import db, create_app, app

app.app_context().push()

def create():
    db.create_all(app=create_app()) # pass the create_app result so Flask-SQLAlchemy gets the configuration.



if __name__=="__main__":
    create()
