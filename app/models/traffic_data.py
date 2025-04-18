from app.utils.db import db
from datetime import datetime


class T_TrafficData(db.Model):
    __tablename__ = 'T_TrafficData'

    id = db.Column(db.Integer, primary_key=True)
    coordinates = db.Column(db.String(50), nullable=False)  # "lat,lng"
    severity = db.Column(db.String(20), nullable=False)  # 'high'/'medium'
    description = db.Column(db.String(200))
    time_from = db.Column(db.String(5))  # "HH:MM"
    time_to = db.Column(db.String(5))  # "HH:MM"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)