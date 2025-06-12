# GitHub Follower Graph

A tool for analyzing connections between GitHub users by building and querying a follower graph.

## Overview

This project allows you to:
- Build a graph of GitHub followers starting from a specific user
- Find the shortest path between two GitHub users
- Get statistics about the graph
- Query paths via a REST API

## Installation

### Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Set up GitHub API token (optional but recommended to avoid rate limits):
   ```
   export GITHUB_TOKEN='your_github_token'
   ```
   You can also create a `.env` file in the project root with:
   ```
   GITHUB_TOKEN=your_github_token
   ```

## Usage

### Building the Graph

The graph needs to be generated before you can query paths or use the API:

```
python builder.py
```

You will be prompted to enter a GitHub username to start the collection. The script will:
- Fetch the user's following list
- Build a directed graph where an edge from A to B means A follows B
- Save the graph to `github_graph.pkl`

The default depth is 3, which means it will collect followers up to 3 levels deep.

### Querying Paths

To find the shortest path between two GitHub users:

```
python query.py
```

You will be prompted to enter:
- Source username
- Target username
- Maximum path length (default is 3)

The script will return the shortest path if one exists within the specified maximum length.

### Getting Statistics

To view basic statistics about the graph:

```
python stats.py
```

This will display:
- Number of nodes (users)
- Number of edges (follows)

### Using the API

The project includes a REST API built with Flask that allows you to query paths programmatically:

1. Start the API server:
   ```
   python api.py
   ```

2. The server will run on `http://localhost:5000` by default

3. Query paths using the following endpoint:
   ```
   GET /path/{user1}/{user2}?max_depth={depth}
   ```
   - `user1`: Source GitHub username
   - `user2`: Target GitHub username
   - `max_depth`: (Optional) Maximum path length, default is 3

4. Example request:
   ```
   GET http://localhost:5000/path/octocat/torvalds?max_depth=4
   ```

5. Response format:
   - Success (200 OK):
     ```json
     {
       "path": ["octocat", "user1", "user2", "torvalds"]
     }
     ```
   - Not found (404 Not Found):
     ```json
     {
       "error": "No path found"
     }
     ```

## Examples

### Finding a path between users

```python
import query

# Load the graph
graph = query.load_graph()

# Check if there's a path from 'octocat' to 'torvalds' with max depth of 4
found, path = query.check_path(graph, 'octocat', 'torvalds', max_depth=4)

if found:
    print(f"Path found: {' -> '.join(path)}")
else:
    print("No path found")
```

### Using the API with curl

```bash
# Find path between 'octocat' and 'torvalds' with default max_depth (3)
curl http://localhost:5000/path/octocat/torvalds

# Find path with custom max_depth
curl http://localhost:5000/path/octocat/torvalds?max_depth=4
```

## Dependencies

- requests: For GitHub API calls
- networkx: For graph operations
- python-dotenv: For loading environment variables
- flask: For the REST API