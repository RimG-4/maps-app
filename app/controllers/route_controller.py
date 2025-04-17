from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
from app.services.route_service import get_route_coordinates

route_bp = Blueprint('route', __name__)

@route_bp.route('/get_route', methods=['POST'])
@login_required
def get_route():
    data = request.get_json()
    from_address = data.get("from")
    to_address = data.get("to")

    if not from_address or not to_address:
        return jsonify({"error": "Нужно указать адреса 'from' и 'to'"}), 400

    try:
        route_coords = get_route_coordinates(from_address, to_address)
        return jsonify({"route": route_coords})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@route_bp.route('/route_form')
@login_required
def show_form():
    return render_template('navigation/route_form.html')

@route_bp.route('/map')
@login_required
def show_map():
    return render_template('navigation/map.html')
