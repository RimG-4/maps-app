from flask import Blueprint, request, jsonify
from app.services.route_service import get_route_coordinates

route_bp = Blueprint('route', __name__)

@route_bp.route('/get_route', methods=['POST'])
def get_route():
    data = request.get_json()
    from_address = data.get("from")
    to_address = data.get("to")

    route_coords = get_route_coordinates(from_address, to_address)
    return jsonify({"route": route_coords})
