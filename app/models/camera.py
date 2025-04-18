from app.utils.db import db


class T_Camera(db.Model):
    __tablename__ = 'T_Camera'

    id = db.Column(db.Integer, primary_key=True)
    coordinates = db.Column(db.String(50), nullable=False)  # "широта,долгота"
    camera_type = db.Column(db.String(20), nullable=False)  # "speed", "traffic_light" и т.д.
    description = db.Column(db.String(100))