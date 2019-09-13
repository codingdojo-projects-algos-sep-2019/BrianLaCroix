from flask import Flask
from flask_sqlalchemy import SQLAlchemy		
from flask_migrate import Migrate
app = Flask(__name__)

# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network_backbone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# an instance of the ORM
db = SQLAlchemy(app)
migrate = Migrate(app, db)