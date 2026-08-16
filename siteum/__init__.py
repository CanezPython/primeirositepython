from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site1.db"
app.config['SECRET_KEY'] = 'e81c1a3801e816e13b7768fd67a64b4f'

database = SQLAlchemy(app)
bcrypt = Bcrypt (app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'


from siteum import routes
