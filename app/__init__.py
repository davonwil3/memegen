
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .authentication.routes import auth_blueprint
from models import db , login_manager
from .api.routes import site
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth

service_account_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'meme-a679b-firebase-adminsdk-bx2vu-37fa442c6b.json'))
cred = credentials.Certificate(service_account_path)
default_app = firebase_admin.initialize_app(cred)

app = Flask(__name__, template_folder='./site/site_templates')
CORS(app)

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.py')
app.config.from_pyfile(config_path)
login_manager.init_app(app)
db.init_app(app)
app.register_blueprint(auth_blueprint)
app.register_blueprint(site)
login_manager.login_view = 'auth.signin'



if __name__ == '__main__':
    app.run(debug=True)
