from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.services.route_service import RouteService
import logging

# Инициализация сервиса
route_bp = Blueprint('route', __name__)
route_service = RouteService()
logger = logging.getLogger(__name__)


@route_bp.route('/get_route', methods=['POST'])
@login_required
def get_route():
    data = request.get_json()
    from_address = data.get("from")
    to_address = data.get("to")

    # Валидация входных данных
    if not from_address or not to_address:
        logger.warning("Попытка построить маршрут без указания адресов")
        return jsonify({"error": "Необходимо указать адреса 'Откуда' и 'Куда'"}), 400

    try:
        # Получаем данные маршрута
        route_data = route_service.get_route(from_address, to_address)

        if not route_data:
            logger.error(f"Не удалось построить маршрут от {from_address} до {to_address}")
            return jsonify({"error": "Не удалось построить маршрут между указанными адресами"}), 400

        # Успешный ответ
        logger.info(f"Успешно построен маршрут: {from_address} -> {to_address}")
        return jsonify({
            "route": route_data['coordinates'],
            "distance": route_data['distance'],
            "time": route_data['time'],
            "from_coords": route_data['from_coords'],
            "to_coords": route_data['to_coords']
        })

    except Exception as e:
        logger.error(f"Ошибка при построении маршрута: {str(e)}")
        return jsonify({
            "error": "Внутренняя ошибка сервера при построении маршрута",
            "details": str(e)
        }), 500


# Сохраняем остальные маршруты без изменений
@route_bp.route('/route_form')
@login_required
def show_form():
    return render_template('navigation/route_form.html')


@route_bp.route('/map')
@login_required
def show_map():
    return render_template('navigation/map.html')

@route_bp.route('/api/traffic', methods=['GET'])
def get_traffic():
    from app.models.traffic_data import T_TrafficData
    traffic = T_TrafficData.query.all()
    return jsonify([{
        'coordinates': t.coordinates,
        'severity': t.severity,
        'description': t.description,
        'time_from': t.time_from,
        'time_to': t.time_to
    } for t in traffic])

@route_bp.route('/api/cameras', methods=['GET'])
def get_cameras():
    from app.models.camera import T_Camera
    cameras = T_Camera.query.all()
    return jsonify([{
        'coordinates': c.coordinates,
        'type': c.camera_type,
        'description': c.description
    } for c in cameras])

@route_bp.route('/api/road_closures', methods=['GET'])
def get_road_closures():
    from app.models.road_closure import T_RoadClosure
    closures = T_RoadClosure.query.all()
    return jsonify([{
        'coordinates': cl.coordinates,
        'type': cl.closure_type,
        'description': cl.description,
        'start_date': cl.start_date.isoformat() if cl.start_date else None,
        'end_date': cl.end_date.isoformat() if cl.end_date else None
    } for cl in closures])