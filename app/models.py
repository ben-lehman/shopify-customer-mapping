from app import db


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    zipcode = db.Column(db.String(10), nullable=False, unique=True)
    count = db.Column(db.Integer, default=1)

    def __init__(self, lat, lng, zipcode):
        self.lat = lat
        self.lng = lng
        self.zipcode = zipcode
        self.count = 1

    @property
    def serialize(self):
        return {
          'id'      : self.id,
          'lat'     : self.lat,
          'lng'     : self.lng,
          'zip'     : self.zipcode,
          'count'   : self.count
        }

    def to_dict(self):
        data = {
            'id'    : self.id,
            'lat'   : self.lat,
            'lng'   : self.lng,
            'zip'   : self.zipcode,
            'count' : self.count
        }

        return data


    def __repr__(self):
        return '<Customer {}>'.format(self.zip)
