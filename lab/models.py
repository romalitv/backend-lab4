from lab.db import db
from sqlalchemy import func


class UserModel(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.String, primary_key=True)
    user_name = db.Column(db.String(128), unique=True, nullable=False)

    record = db.relationship("RecordModel", back_populates="user", lazy="dynamic")
    category = db.relationship("CategoryModel", back_populates="user")

class CategoryModel(db.Model):
    __tablename__ = 'category'

    category_id = db.Column(db.String, primary_key=True)
    category_name = db.Column(db.String(128), unique=True, nullable=False)
    is_common = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.String,
                        db.ForeignKey('user.user_id'),
                        unique=False,
                        nullable=True)
    record = db.relationship("RecordModel", back_populates="category", lazy="dynamic")
    user = db.relationship("UserModel", back_populates="category")

class RecordModel(db.Model):
    __tablename__ = 'record'

    record_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String,
                        db.ForeignKey('user.user_id'),
                        unique=False,
                        nullable=False
                        )
    category_id = db.Column(db.String,
                            db.ForeignKey('category.category_id'),
                            unique=False,
                            nullable=False
                            )
    time = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    amount_of_money = db.Column(db.Float(), unique=False, nullable=False)

    user = db.relationship("UserModel", back_populates="record")
    category = db.relationship("CategoryModel", back_populates="record")