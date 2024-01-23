import uuid

from flask import jsonify, request, abort
from flask_smorest import Blueprint
from marshmallow import ValidationError
from lab.models import UserModel, db
from lab.entities import UserSchema
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256

blp_user = Blueprint('user', __name__, description="Operations related to users")
user_schema = UserSchema()

@blp_user.post('/register_user')
def create_user():
    user = request.json
    try:
        data = user_schema.load(user)
    except ValidationError as e:
        return jsonify(e.messages), 400

    data['user_id'] = uuid.uuid4().hex
    data['user_password'] = pbkdf2_sha256.hash(data['user_password'])
    user = UserModel(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        abort(400, message="failed creating user")
    return user_schema.dump(user)

@blp_user.post('/login_user')
def login_user():
    user = request.json
    try:
        data = user_schema.load(user)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user = UserModel.query.filter_by(user_name=data['user_name']).first()
    if user and pbkdf2_sha256.verify(data['user_password'], user.user_password):
        access_token = create_access_token(identity=user.user_id)
        return jsonify(access_token), 200
    else:
        abort(400, message="wrong name or password")


@blp_user.get('/users')
@jwt_required()
def get_users():
    data = user_schema.dump(UserModel.query.all(), many=True)
    return jsonify(data)


@blp_user.get('/user')
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = UserModel.query.get(user_id)
    try:
        return jsonify(user_schema.dump(user)), 200
    except Exception :
       abort(400, "cannot find users")


@blp_user.delete('/user')
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    print("JWT Identity:", user_id)
    user = UserModel.query.get(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    except Exception:
        abort(400, message="failed deleting user")