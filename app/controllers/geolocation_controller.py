from flask import Blueprint, request, jsonify, session
from app.models.user_settings import UserSettings
from app import db
from datetime import datetime

geolocation_bp = Blueprint('geolocation', __name__)


@geolocation_bp.route('/api/geolocation/permission', methods=['POST'])
def handle_permission():
    data = request.json
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    settings = UserSettings.query.filter_by(user_id=user_id).first()
    if not settings:
        settings = UserSettings(user_id=user_id)
        db.session.add(settings)

    if data.get('allowed', False):
        settings.enable_geolocation()
    else:
        settings.disable_geolocation()

    db.session.commit()
    return jsonify({"status": "success"})


@geolocation_bp.route('/api/geolocation/update', methods=['POST'])
def update_location():
    data = request.json
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "Not authenticated"}), 401

    settings = UserSettings.query.filter_by(user_id=user_id).first()
    if not settings:
        return jsonify({"error": "Settings not found"}), 404

    if settings.geolocation_enabled:
        try:
            settings.update_location(
                lat=data['lat'],
                lng=data['lng']
            )
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    return jsonify({"success": False, "error": "Geolocation disabled"})