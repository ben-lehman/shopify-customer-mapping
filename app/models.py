from app import (db, ma)


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    address1 = db.Column(db.String(120))

    @property
    def serialize(self):
        return {
          'id'      : self.id,
          'name'    : self.name,
          'lat'     : self.lat,
          'lng'     : self.lng,
          'address1': self.address1
        }

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lng': self.lng,
            'address1': self.address1
        }

        return data


    def __repr__(self):
        return '<Customer {}>'.format(self.name)

class CustomerSchema(ma.ModelSchema):
    class Meta:
        model = Customer
