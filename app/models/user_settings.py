from app import db
from datetime import datetime


class UserSettings(db.Model):
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    geolocation_enabled = db.Column(db.Boolean, default=False)
    last_latitude = db.Column(db.Float)
    last_longitude = db.Column(db.Float)
    location_history = db.Column(db.JSON)  # Новое поле для истории

    def enable_geolocation(self):
        self.geolocation_enabled = True
        db.session.commit()

    def disable_geolocation(self):
        self.geolocation_enabled = False
        db.session.commit()

    def update_location(self, lat, lng):
        self.last_latitude = lat
        self.last_longitude = lng

        # Если история пустая, создаём список
        if self.location_history is None:
            self.location_history = []

        # Добавляем новую запись
        self.location_history.append({
            "lat": lat,
            "lng": lng,
            "timestamp": datetime.now().isoformat()
        })

        db.session.commit()