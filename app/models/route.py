from app.utils.db import db
from app.models.traffic_data import T_TrafficData
from app.models.trip_history import T_TripHistory

class T_Route(db.Model):
    __tablename__ = 'T_Route'
    routeID = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)

    trips = db.relationship('T_TripHistory', back_populates='route')
    traffic = db.relationship('T_TrafficData', back_populates='route')
