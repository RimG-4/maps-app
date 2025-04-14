from flask import Blueprint, render_template

navigation_bp = Blueprint('navigation', __name__)

@navigation_bp.route('/map')
def show_map():
    return render_template('ufa_map.html')

