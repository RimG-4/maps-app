from flask import Blueprint, request, jsonify
import requests

geolocation_bp = Blueprint('geolocation', __name__)

@geolocation_bp.route('/get_address')
def get_address():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if lat and lon:
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
            headers = {'User-Agent': 'maps/1.0 (lemonsensei04@gmail.com)'}
            response = requests.get(url, headers=headers)
            data = response.json()
            address = data.get("display_name", "Адрес не найден")
            return jsonify({'address': address})
        except Exception as e:
            return jsonify({'error': f'Ошибка при получении адреса: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Неверные координаты'}), 400
