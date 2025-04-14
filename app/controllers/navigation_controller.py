from flask import Blueprint, render_template

# Создаём блюпринт для навигации
navigation_bp = Blueprint('navigation', __name__)

# Роут для отображения карты
@navigation_bp.route('/map')
def show_map():
    return render_template('ufa_map.html')
