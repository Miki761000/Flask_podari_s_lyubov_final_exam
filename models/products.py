from db import db


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_code = db.Column(db.String(100), nullable=False)
    product_name = db.Column(db.String(500), nullable=False)
    product_quantity = db.Column(db.Integer, default=0, nullable=True)
    product_delivery_price = db.Column(db.Float, default=0, nullable=True)
    product_description = db.Column(db.String, default="", nullable=True)
    product_image = db.Column(db.String(255), nullable=False)

    product_type_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    category = db.relationship("CategoryModel", cascade="all, delete")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel", cascade="all, delete")
