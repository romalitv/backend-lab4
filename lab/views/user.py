import uuid

from flask import jsonify, request, abort
from flask_smorest import Blueprint
from marshmallow import ValidationError
from lab.models import UserModel, db
from lab.entities import UserSchema

blp_user = Blueprint('user', __name__, description="Operations related to users")
user_schema = UserSchema()

@blp_user.post('/user')
def create_user():
    user = request.json
    try:
        data = UserSchema().load(user)
    except ValidationError as e:
        return jsonify(e.messages), 400

    data['user_id'] = uuid.uuid4().hex
    user = UserModel(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception :
        abort(400, message="failed creating user")

    return user_schema.dump(user)




@blp_user.get('/users')
def get_users():
    data = user_schema.dump(UserModel.query.all(), many=True)
    return jsonify(data)


@blp_user.get('/user/<user_id>')
def get_user(user_id):
    user = UserModel.query.get(user_id)
    try:
        return jsonify(user_schema.dump(user)), 200
    except Exception :
       abort(400, "cannot find users")


@blp_user.delete('/user/<user_id>')
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 200
    except Exception:
        abort(400, message="failed deleting user")