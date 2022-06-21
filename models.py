# from sqlalchemy.dialects.postgresql import JSON

from app_main import db


class ItemWB(db.Model):
    __tablename__ = 'itemsWB'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    brand = db.Column(db.String(100))
    salePriceU = db.Column(db.Float)
    rating = db.Column(db.Float)
    link = db.Column(db.String(100))

    def __init__(self, id, name, brand, salePriceU, rating, link):
        self.id = id
        self.name = name
        self.brand = brand
        self.salePriceU = salePriceU
        self.rating = rating
        self.link = link

    def __repr__(self):
        return '<id {}>'.format(self.id)


# class ItemOZON(db.Model):
#     __tablename__ = 'itemsOZON'

#     id = db.Column(db.Integer, primary_key=True)
#     brand = db.Column(db.String(100))
#     title = db.Column(db.String(100), index=True, unique=True)
#     final_price = db.Column(db.Float)
#     link = db.Column(db.String(100), index=True, unique=True)
#     rating = db.Column(db.Float)

#     def __init__(self, id, brand, title, final_price, link, rating):
#         self.id = id
#         self.brand = brand
#         self.title = title
#         self.final_price = final_price
#         self.link = link
#         self.rating = rating

#     def __repr__(self):
#         return '<id {}>'.format(self.id)
