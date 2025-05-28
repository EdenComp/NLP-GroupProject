import requests
import time
import networkx as nx
import pickle
import os
from dotenv import load_dotenv

load_dotenv()

# Constants
BASE_URL = 'https://api.github.com/users/'
GRAPH_FILE = 'github_graph.pkl'
TOKEN = os.getenv("GITHUB_TOKEN")  # Set this environment variable before running

HEADERS = {
    'Accept': 'application/vnd.github.v3+json'
}
if TOKEN:
    HEADERS['Authorization'] = f'token {TOKEN}'

def get_connections(username, connection_type='following'):
    url = f"{BASE_URL}{username}/{connection_type}?per_page=100"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch {connection_type} for {username} ({response.status_code})")
        return []
    return [user['login'] for user in response.json()]

def load_graph():
    if os.path.exists(GRAPH_FILE):
        with open(GRAPH_FILE, 'rb') as f:
            print("Loading existing graph...")
            return pickle.load(f)
    print("No existing graph found. Creating a new one.")
    return nx.DiGraph()

def save_graph(graph):
    with open(GRAPH_FILE, 'wb') as f:
        pickle.dump(graph, f)
    print(f"Graph saved to {GRAPH_FILE}")

def build_graph(start_user, depth=1):
    G = load_graph()
    visited = set()  # track processed users only
    queue = [(start_user, 0)]  # always start from this user

    while queue:
        user, level = queue.pop(0)
        if user in visited or level > depth:
            continue
        visited.add(user)

        following = get_connections(user, 'following')
        print(f"Following of {user}: {following}")
        for f in following:
            G.add_edge(user.lower(), f.lower())

        queue.extend([(f, level + 1) for f in following])
        time.sleep(0.5)  # Respect GitHub rate limits

    save_graph(G)


# Run the script
if __name__ == "__main__":
    if not TOKEN:
        print("⚠️ WARNING: No GitHub token found. You are limited to 60 requests/hour.")
        print("Set a token with: export GITHUB_TOKEN='your_token_here'")

    username = input("Enter username to start collection: ").strip().lower()
    build_graph(username, depth=2)
