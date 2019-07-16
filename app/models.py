from app import db


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    zipcode = db.Column(db.String(10))

    @property
    def serialize(self):
        return {
          'id'      : self.id,
          'lat'     : self.lat,
          'lng'     : self.lng,
          'zip'     : self.zipcode
        }

    def to_dict(self):
        data = {
            'id'    : self.id,
            'lat'   : self.lat,
            'lng'   : self.lng,
            'zip'   : self.zipcode
        }

        return data


    def __repr__(self):
        return '<Customer {}>'.format(self.name)
