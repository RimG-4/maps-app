from flask import Blueprint, render_template
from flask_login import login_required

# Создаём блюпринт для навигации
navigation_bp = Blueprint('navigation', __name__)

# Роут для отображения карты
@login_required
@navigation_bp.route('/map')
def show_map():
    return render_template('navigation/map.html')
