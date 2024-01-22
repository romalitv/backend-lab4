import uuid

from flask import jsonify, request, abort
from flask_smorest import Blueprint
from marshmallow import ValidationError
from lab.models import db, CategoryModel, UserModel
from lab.entities import CategorySchema

blp_category = Blueprint('category', __name__, description='Operations related to category')
category_schema = CategorySchema()


@blp_category.post("/category")
def create_category():
    category = request.json

    user_id = category.get('user_id', None)

    if user_id is not None:
        user = UserModel.query.get(user_id)
        if user is None:
            return jsonify({'error': 'Invalid user_id'}), 400
    else:
        user_id = None

    try:
        data = category_schema.load(category)
    except ValidationError as e:
        return jsonify(e.messages), 401

    is_common = data.get("is_common", False)

    data["is_common"] = is_common
    data["category_id"] = uuid.uuid4().hex
    data["user_id"] = user_id
    category = CategoryModel(**data)

    try:
        db.session.add(category)
        db.session.commit()
    except Exception:
        abort(401, message="failed creating category")

    return category_schema.dump(category)

@blp_category.get("/category")
def get_categories():
    user_id = request.args.get("user_id")

    if user_id:
        categories = CategoryModel.query.filter(CategoryModel.is_common | (CategoryModel.user_id == user_id)).all()
    else:
        categories = CategoryModel.query.filter_by(is_common=True).all()

    data = category_schema.dump(categories, many=True)
    return jsonify(data)

@blp_category.delete("/category/<category_id>")
def delete_category(category_id):
    category = CategoryModel.query.get(category_id)
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify(category_schema.dump(category)), 200
    except Exception:
        abort(400, message="failed deleting category")