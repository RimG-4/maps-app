from flask import Blueprint, jsonify
from app.models.traffic_data import T_TrafficData

traffic_bp = Blueprint('traffic', __name__)

@traffic_bp.route('/traffic', methods=['GET'])
def get_traffic():
    traffic_data = T_TrafficData.query.all()
    return jsonify([{
        'coordinates': [float(c) for c in t.coordinates.split(',')],
        'severity': t.severity,
        'delay': t.delay
    } for t in traffic_data])