from flask import Flask, request, jsonify
import query

app = Flask(__name__)

# Load the graph once at startup to avoid loading it on every request
graph = query.load_graph()

@app.route('/path/<user1>/<user2>', methods=['GET'])
def get_path(user1, user2):
    # Get max_depth from query parameter, default to 3
    max_depth = request.args.get('max_depth', default=3, type=int)

    # Check path between users using the pre-loaded graph
    found, path = query.check_path(graph, user1.lower(), user2.lower(), max_depth=max_depth)

    if found:
        return jsonify({"path": path})
    else:
        return jsonify({"error": "No path found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
