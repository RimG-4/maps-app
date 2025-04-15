import requests
import networkx as nx
import osmnx as ox

G = ox.load_graphml("ufa_roads.graphml")

def geocode_address(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
    response = requests.get(url)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None

def get_route_coordinates(from_address, to_address):
    from_coords = geocode_address(from_address)
    to_coords = geocode_address(to_address)

    if not from_coords or not to_coords:
        return []

    orig_node = ox.distance.nearest_nodes(G, from_coords[1], from_coords[0])
    dest_node = ox.distance.nearest_nodes(G, to_coords[1], to_coords[0])

    route = nx.shortest_path(G, orig_node, dest_node, weight='length')
    return [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
