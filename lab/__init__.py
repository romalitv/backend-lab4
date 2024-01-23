import os
import lab.jwtkey

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .db import db
from lab.models import UserModel, RecordModel, CategoryModel

from .views.user import blp_user
from .views.category import blp_category
from .views.record import blp_record



app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

db.init_app(app)

jwt = JWTManager(app)

migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

app.register_blueprint(blp_category)
app.register_blueprint(blp_record)
app.register_blueprint(blp_user)
