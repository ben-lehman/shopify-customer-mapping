from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    address1 = db.Column(db.String(120))

    def __repr__(self):
        return '<Customer {}>'.format(self.name)

