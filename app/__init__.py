
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .authentication.routes import auth
from models import db , login_manager
from .api.routes import site


app = Flask(__name__, template_folder='./site/site_templates')

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.py')
app.config.from_pyfile(config_path)
login_manager.init_app(app)
db.init_app(app)
app.register_blueprint(auth)
app.register_blueprint(site)
login_manager.login_view = 'auth.signin'



if __name__ == '__main__':
    app.run(debug=True)
