from sqlalchemy.dialects.postgresql import JSONB

from app_main import db
# from main1 import db


class ItemWB(db.Model):
    __tablename__ = 'itemsWB'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    brand = db.Column(db.String(200))
    sale_price = db.Column(db.Float)
    rating = db.Column(db.Float)
    link = db.Column(db.String(100))
    history = db.Column(JSONB)

    def __init__(self, id, name, brand, sale_price, rating, link, history):
        self.id = id
        self.name = name
        self.brand = brand
        self.sale_price = sale_price
        self.rating = rating
        self.link = link
        self.history = history

    def __repr__(self):
        return '<id {}>'.format(self.id)
