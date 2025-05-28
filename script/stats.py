import pickle
import networkx as nx
import os

GRAPH_FILE = 'github_graph.pkl'

def load_graph():
    if not os.path.exists(GRAPH_FILE):
        print(f"Graph file '{GRAPH_FILE}' not found. Run the builder script first.")
        exit(1)
    with open(GRAPH_FILE, 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    G = load_graph()
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    print("📈 GitHub Follower Graph Stats:")
    print(f"  Nodes (users): {num_nodes}")
    print(f"  Edges (follows): {num_edges}")
