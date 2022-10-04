from flask import Flask

from mock_graph_data import edges
from os_graph import Graph
import sys

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Graph search demo with OpenSearch</p>"

@app.route('/paths/<start_id>:<end_id>/<int:distance>')
# e.g. http://localhost:5001/paths/1034:1808/9
# e.g. http://localhost:5001/paths/1034:963/4
def paths(start_id, end_id, distance):
    print(f'Requests path from {start_id} to {end_id} with distance = {distance}')
    paths, time_elapsed = graph.get_all_paths(start_id, end_id, distance)
    result = {
        '_search_details': f'Find path between {start_id} and {end_id} with distance = {distance}',
        '_search_performance': f'Searched {graph.repo.size()} nodes in {time_elapsed} seconds.',
        'paths_found': len(paths),
        'valid_paths': paths
    }
    return result

@app.route('/radial/<node_id>/<int:degree>')
# e.g. http://localhost:5001/radial/1035/3
def radial(node_id, degree):
    print(f'Requests radial graph from {node_id} within {degree} degree(s)')
    node_radial, time_elapsed = graph.get_radial_data(node_id, degree)
    result = {
        '_search_details': f'Find node {node_id} neighborhood within {degree} degree(s)',
        '_search_performance': f'Searched {graph.repo.size()} nodes in {time_elapsed} seconds.',
        'node_radial': node_radial,
    }
    return result


if __name__ == "__main__":
    global graph
    graph = Graph(sys.argv[1])
    app.run(host='0.0.0.0', port=5001, debug=True)
