import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from app.models.traffic_data import T_TrafficData
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import logging


class RouteService:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="route-app")
        self.address_cache = {}
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self._graph = None

    @property
    def graph(self):
        if self._graph is None:
            try:
                self.logger.info("Загрузка графа дорог...")
                self._graph = ox.load_graphml("ufa_roads.graphml")
                self.logger.info("Граф дорог успешно загружен")
            except Exception as e:
                self.logger.error(f"Ошибка загрузки графа: {str(e)}")
                raise
        return self._graph

    def get_traffic_delay(self, route_coords):
        """Получаем задержки для маршрута"""
        traffic_points = T_TrafficData.query.all()
        total_delay = 0

        for tp in traffic_points:
            lat, lon = map(float, tp.coordinates.split(','))
            for route_point in route_coords:
                distance = great_circle((lat, lon), route_point).meters
                if distance < 100:  # 100 метров радиус влияния пробки
                    total_delay += tp.delay
                    break

        return total_delay

    def geocode_address(self, address):
        if address in self.address_cache:
            return self.address_cache[address]

        try:
            location = self.geolocator.geocode(address, timeout=10)
            if location:
                coords = (location.latitude, location.longitude)
                self.address_cache[address] = coords
                return coords
            else:
                self.logger.warning(f"Не удалось найти координаты для адреса: {address}")
                return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            self.logger.error(f"Ошибка геокодирования адреса '{address}': {e}")
            return None

    def find_path(self, from_coords, to_coords):
        """Поиск пути с обработкой ошибок (адаптировано из вашего кода)"""
        try:
            orig_node = ox.distance.nearest_nodes(self.graph,
                                                  X=from_coords[1],
                                                  Y=from_coords[0])
            dest_node = ox.distance.nearest_nodes(self.graph,
                                                  X=to_coords[1],
                                                  Y=to_coords[0])

            route = nx.shortest_path(self.graph, orig_node, dest_node, weight="length")
            return [(self.graph.nodes[node]["y"], self.graph.nodes[node]["x"]) for node in route]

        except nx.NetworkXNoPath:
            self.logger.warning(f"Нет пути между точками {from_coords} и {to_coords}")
            return []
        except Exception as e:
            self.logger.error(f"Ошибка при построении маршрута: {e}")
            return []


    def calculate_route_stats(self, route_coords):
        if not route_coords or len(route_coords) < 2:
            return {'distance_km': 0, 'time_minutes': 0}

        total_distance = sum(
            great_circle(route_coords[i], route_coords[i + 1]).meters
            for i in range(len(route_coords) - 1))

        # Расчет времени с базовой скоростью 50 км/ч
        time_minutes = round((total_distance / 1000) / 50 * 60)  # км / (км/ч) * 60

        # Добавляем задержки от пробок
        traffic_delay = self.get_traffic_delay(route_coords)
        time_minutes += traffic_delay

        return {
            'distance_km': round(total_distance / 1000, 2),
            'time_minutes': int(time_minutes),
            'traffic_delay': traffic_delay
        }

    def get_route(self, from_address, to_address):
        """Основной метод получения маршрута (комбинированный)"""
        from_coords = self.geocode_address(from_address)
        to_coords = self.geocode_address(to_address)

        if not from_coords or not to_coords:
            self.logger.warning("Один из адресов не удалось геокодировать")
            return None

        route_coords = self.find_path(from_coords, to_coords)
        if not route_coords:
            return None

        stats = self.calculate_route_stats(route_coords)

        return {
            'coordinates': route_coords,
            'distance': stats['distance_km'],
            'time': stats['time_minutes'],
            'from_coords': from_coords,
            'to_coords': to_coords
        }