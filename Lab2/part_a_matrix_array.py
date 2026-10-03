"""Part (a): Dijkstra's algorithm using a matrix and an array."""


INFINITY = float("inf")


def find_nearest_unvisited_vertex(distances, visited):
    """Return the unvisited vertex with the smallest known distance."""
    smallest_distance = INFINITY
    nearest_vertex = -1

    for vertex in range(len(distances)):
        vertex_is_unvisited = visited[vertex] == False
        distance_is_smaller = distances[vertex] < smallest_distance

        if vertex_is_unvisited and distance_is_smaller:
            smallest_distance = distances[vertex]
            nearest_vertex = vertex

    return nearest_vertex


def dijkstra(adjacency_matrix, source):
    """
    Find the shortest distance from source to every vertex.

    adjacency_matrix[u][v] is the weight of edge u -> v.
    None means that there is no edge. Edge weights must be non-negative.

    Returns two arrays:
    - distances[v] is the shortest distance from source to v.
    - previous[v] is the vertex before v on its shortest path.
    """
    number_of_vertices = len(adjacency_matrix)

    if source < 0 or source >= number_of_vertices:
        raise ValueError("The source vertex is outside the graph.")

    distances = []
    previous = []
    visited = []

    for vertex in range(number_of_vertices):
        distances.append(INFINITY)
        previous.append(None)
        visited.append(False)

    distances[source] = 0

    for step in range(number_of_vertices):
        current_vertex = find_nearest_unvisited_vertex(distances, visited)

        # -1 means that every remaining vertex is unreachable.
        if current_vertex == -1:
            break

        visited[current_vertex] = True

        # An adjacency matrix requires us to inspect every possible neighbour.
        for neighbour in range(number_of_vertices):
            edge_weight = adjacency_matrix[current_vertex][neighbour]

            if edge_weight is None:
                continue

            if edge_weight < 0:
                raise ValueError("Dijkstra's algorithm cannot use negative edges.")

            if visited[neighbour] == True:
                continue

            new_distance = distances[current_vertex] + edge_weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current_vertex

    return distances, previous


def make_path(previous, source, destination):
    """Build one shortest path from source to destination."""
    path_backwards = []
    current_vertex = destination

    while current_vertex is not None:
        path_backwards.append(current_vertex)

        if current_vertex == source:
            break

        current_vertex = previous[current_vertex]

    if path_backwards[-1] != source:
        return []

    path = []

    for position in range(len(path_backwards) - 1, -1, -1):
        path.append(path_backwards[position])

    return path


def print_example():
    """Run Dijkstra's algorithm on a small example graph."""
    graph = [
        [None, 10,   3, None, None],
        [None, None, 1,    2, None],
        [None,   4, None,  8,    2],
        [None, None, None, None, 7],
        [None, None, None,   9, None],
    ]

    source = 0
    distances, previous = dijkstra(graph, source)

    print("Source vertex:", source)
    print()

    for destination in range(len(graph)):
        path = make_path(previous, source, destination)

        print("Destination:", destination)
        print("Distance:", distances[destination])
        print("Path:", path)
        print()


if __name__ == "__main__":
    print_example()
