"""Part (b): Dijkstra's algorithm using adjacency lists and a minimizing heap."""


INFINITY = float("inf")


class MinHeap:
    """
    A binary minimizing heap of vertices, ordered by their distance.

    The heap is stored in an array. For the item at position i:
    - its parent is at position (i - 1) // 2
    - its children are at positions 2 * i + 1 and 2 * i + 2

    position[v] remembers where vertex v is inside the heap array. This lets
    decrease_key find a vertex in O(1) time instead of searching the heap.
    """

    def __init__(self, number_of_vertices):
        self.vertices = []
        self.keys = []
        self.position = []

        for vertex in range(number_of_vertices):
            self.position.append(-1)

    def is_empty(self):
        return len(self.vertices) == 0

    def contains(self, vertex):
        return self.position[vertex] != -1

    def swap(self, first, second):
        """Swap two heap positions and update the position array."""
        first_vertex = self.vertices[first]
        second_vertex = self.vertices[second]

        self.vertices[first] = second_vertex
        self.vertices[second] = first_vertex

        first_key = self.keys[first]
        self.keys[first] = self.keys[second]
        self.keys[second] = first_key

        self.position[second_vertex] = first
        self.position[first_vertex] = second

    def sift_up(self, index):
        """Move an item up until its parent is not larger. O(log V)."""
        while index > 0:
            parent = (index - 1) // 2

            if self.keys[parent] <= self.keys[index]:
                break

            self.swap(index, parent)
            index = parent

    def sift_down(self, index):
        """Move an item down until both children are not smaller. O(log V)."""
        size = len(self.vertices)

        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index

            if left_child < size and self.keys[left_child] < self.keys[smallest]:
                smallest = left_child

            if right_child < size and self.keys[right_child] < self.keys[smallest]:
                smallest = right_child

            if smallest == index:
                break

            self.swap(index, smallest)
            index = smallest

    def insert(self, vertex, key):
        """Add a vertex to the heap. O(log V)."""
        self.vertices.append(vertex)
        self.keys.append(key)
        self.position[vertex] = len(self.vertices) - 1
        self.sift_up(len(self.vertices) - 1)

    def extract_min(self):
        """Remove and return (vertex, key) with the smallest key. O(log V)."""
        smallest_vertex = self.vertices[0]
        smallest_key = self.keys[0]
        last_index = len(self.vertices) - 1

        self.swap(0, last_index)
        self.vertices.pop()
        self.keys.pop()
        self.position[smallest_vertex] = -1

        if not self.is_empty():
            self.sift_down(0)

        return smallest_vertex, smallest_key

    def decrease_key(self, vertex, new_key):
        """Lower the key of a vertex that is already in the heap. O(log V)."""
        index = self.position[vertex]
        self.keys[index] = new_key
        self.sift_up(index)


def dijkstra_with_heap(adjacency_list, source, heap_class=MinHeap):
    """
    Find the shortest distance from source to every vertex.

    adjacency_list[u] is a list of (v, weight) pairs, one for each edge u -> v.
    Edge weights must be non-negative.

    heap_class lets the experiment pass in a MinHeap that also counts its
    operations. Normal callers can ignore it.

    Returns two arrays:
    - distances[v] is the shortest distance from source to v.
    - previous[v] is the vertex before v on its shortest path.
    """
    number_of_vertices = len(adjacency_list)

    if source < 0 or source >= number_of_vertices:
        raise ValueError("The source vertex is outside the graph.")

    distances = []
    previous = []

    for vertex in range(number_of_vertices):
        distances.append(INFINITY)
        previous.append(None)

    distances[source] = 0

    # Put every vertex into the heap, keyed by its current distance.
    # The source goes in first with key 0, so it is the root of the heap.
    # The other vertices all have key infinity, so no sifting is needed.
    heap = heap_class(number_of_vertices)
    heap.insert(source, 0)

    for vertex in range(number_of_vertices):
        if vertex != source:
            heap.insert(vertex, INFINITY)

    while not heap.is_empty():
        current_vertex, current_distance = heap.extract_min()

        # Every vertex still in the heap is unreachable from the source.
        if current_distance == INFINITY:
            break

        # An adjacency list only stores the edges that really exist,
        # so this loop runs once per outgoing edge of current_vertex.
        for neighbour, edge_weight in adjacency_list[current_vertex]:
            if edge_weight < 0:
                raise ValueError("Dijkstra's algorithm cannot use negative edges.")

            # Vertices no longer in the heap already have their final distance.
            if not heap.contains(neighbour):
                continue

            new_distance = current_distance + edge_weight

            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current_vertex
                heap.decrease_key(neighbour, new_distance)

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


def matrix_to_adjacency_list(adjacency_matrix):
    """Convert a part (a) adjacency matrix into an array of adjacency lists."""
    adjacency_list = []

    for row in adjacency_matrix:
        neighbours = []

        for column in range(len(row)):
            if row[column] is not None:
                neighbours.append((column, row[column]))

        adjacency_list.append(neighbours)

    return adjacency_list


def print_example():
    """Run Dijkstra's algorithm on the same example graph as part (a)."""
    graph = [
        [(1, 10), (2, 3)],
        [(2, 1), (3, 2)],
        [(1, 4), (3, 8), (4, 2)],
        [(4, 7)],
        [(3, 9)],
    ]

    source = 0
    distances, previous = dijkstra_with_heap(graph, source)

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
