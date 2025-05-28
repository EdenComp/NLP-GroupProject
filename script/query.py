import pickle
import networkx as nx
import os

GRAPH_FILE = 'github_graph.pkl'

def load_graph():
    if not os.path.exists(GRAPH_FILE):
        print(f"Graph file '{GRAPH_FILE}' not found. Please run the builder first.")
        exit(1)
    with open(GRAPH_FILE, 'rb') as f:
        print("Loading graph...")
        return pickle.load(f)

def check_path(graph, source, target, max_depth=3):
    if source not in graph:
        print(f"User '{source}' not found in graph.")
        return False, []
    if target not in graph:
        print(f"User '{target}' not found in graph.")
        return False, []

    try:
        path = nx.shortest_path(graph, source=source, target=target)
        if len(path) - 1 <= max_depth:
            return True, path
        else:
            print(f"A path exists but is longer than max_depth={max_depth}.")
    except nx.NetworkXNoPath:
        print("No path found between users.")
    return False, []

# Example usage
if __name__ == "__main__":
    G = load_graph()
    user1 = input("Enter source username: ").strip().lower()
    user2 = input("Enter target username: ").strip().lower()
    max_depth = input("Enter max path length (default=3): ").strip()
    max_depth = int(max_depth) if max_depth.isdigit() else 3

    found, path = check_path(G, user1, user2, max_depth=max_depth)
    if found:
        print(f"✅ Path found ({len(path) - 1} steps): {' -> '.join(path)}")
    else:
        print("❌ No path within the allowed depth.")
