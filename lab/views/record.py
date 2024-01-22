import uuid

from flask import jsonify, request, abort
from flask_smorest import Blueprint
from marshmallow import ValidationError
from lab import CategoryModel, UserModel, db, RecordModel
from datetime import datetime
from lab.entities import RecordSchema

blp_record = Blueprint('record', __name__, description="Record operations")
record_schema = RecordSchema()

@blp_record.post('/record')
def create_record():
    record = request.json
    try:
        data = record_schema.load(record)
    except ValidationError as e:
        return jsonify(e.messages), 400

    data['record_id'] = uuid.uuid4().hex
    data['time'] = datetime.now()
    user = UserModel.query.get(record['user_id'])
    category = CategoryModel.query.get(record['category_id'])
    if category is not None and user is not None:
        if user.user_id != category.user_id and category.user_id is not None:
            abort(400, 'User and category do not match')
        data["user_id"] = user.user_id
        data["category_id"] = category.category_id
    record = RecordModel(**data)
    try:
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        abort(400, str(e))

    return record_schema.dump(record)

@blp_record.get('/record/<record_id>')
def get_record(record_id):
    record = RecordModel.query.get(record_id)
    try:
        return jsonify(record_schema.dump(record)), 200
    except Exception as e:
        abort(400, e.message)

@blp_record.delete('/record/<record_id>')
def delete_record(record_id):
    record = RecordModel.query.get(record_id)
    try:
        db.session.delete(record)
        db.session.commit()
        return jsonify(record_schema.dump(record))
    except Exception as e:
        abort(400, e.message)



@blp_record.get('/record')
def get_records():
    data = request.get_json()
    user_id = data.get('user_id', None)
    category_id = data.get('category_id', None)

    if user_id is None and category_id is None:
        return jsonify({'error': 'At least one parameter (user_id or category_id) is required'}), 400

    query = RecordModel.query
    if user_id is not None:
        query = query.filter_by(user_id=user_id)
    if category_id is not None:
        query = query.filter_by(category_id=category_id)

    try:
        records = query.all()
    except Exception as e:
        return jsonify(error=str(e)), 400

    return jsonify(record_schema.dump(records, many=True)), 200