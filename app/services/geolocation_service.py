from app.models.user_settings import UserSettings

class GeolocationService:
    @staticmethod
    def handle_permission_response(user_id, allowed):
        settings = UserSettings.query.filter_by(user_id=user_id).first()
        if allowed:
            settings.enable_geolocation()
        else:
            settings.disable_geolocation()
        return settings

    @staticmethod
    def update_user_location(user_id, lat, lng):
        settings = UserSettings.query.filter_by(user_id=user_id).first()
        if settings and settings.geolocation_enabled:
            settings.update_location(lat, lng)
            return True
        return False