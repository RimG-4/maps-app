from flask import Blueprint, render_template
from flask_login import login_required

# Создаём блюпринт для навигации
navigation_bp = Blueprint('navigation', __name__)

# Роут для отображения карты
@navigation_bp.route('/map')
@login_required
def show_map():
    return render_template('ufa_map.html')
