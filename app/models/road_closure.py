from app.utils.db import db


class T_RoadClosure(db.Model):
    __tablename__ = 'T_RoadClosure'

    id = db.Column(db.Integer, primary_key=True)
    coordinates = db.Column(db.String(50), nullable=False)  # "широта,долгота"
    closure_type = db.Column(db.String(20), nullable=False)  # "ремонт", "авария" и т.д.
    description = db.Column(db.String(200))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)