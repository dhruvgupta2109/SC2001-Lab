"""Run the empirical time-complexity experiments for part (b)."""

import csv
import math
import random
import time
from pathlib import Path

import matplotlib.pyplot as plt

from part_a_experiment import make_random_connected_graph
from part_b_list_heap import MinHeap, dijkstra_with_heap, matrix_to_adjacency_list


RANDOM_SEED = 42
NUMBER_OF_REPEATS = 5

THIS_FOLDER = Path(__file__).resolve().parent
RESULTS_FOLDER = THIS_FOLDER / "results"
RESULTS_FILE = RESULTS_FOLDER / "part_b_results.csv"


def make_random_connected_adjacency_list(number_of_vertices, number_of_edges, random_generator):
    """
    Create a connected, undirected graph as an array of adjacency lists.

    This version never builds a V by V matrix, so it can create large sparse
    graphs (for example V = 50,000) that would not fit in a matrix.
    """
    smallest_edge_count = number_of_vertices - 1
    largest_edge_count = number_of_vertices * (number_of_vertices - 1) // 2

    if number_of_edges < smallest_edge_count:
        raise ValueError("A connected graph needs at least V - 1 edges.")

    if number_of_edges > largest_edge_count:
        raise ValueError("The requested graph has too many edges.")

    adjacency_list = []

    for vertex in range(number_of_vertices):
        adjacency_list.append([])

    used_edges = set()

    # First add a chain. This guarantees that the graph is connected.
    for vertex in range(number_of_vertices - 1):
        next_vertex = vertex + 1
        weight = random_generator.randint(1, 100)

        adjacency_list[vertex].append((next_vertex, weight))
        adjacency_list[next_vertex].append((vertex, weight))
        used_edges.add((vertex, next_vertex))

    # Then add random extra edges until the requested number is reached.
    while len(used_edges) < number_of_edges:
        first_vertex = random_generator.randrange(number_of_vertices)
        second_vertex = random_generator.randrange(number_of_vertices)

        if first_vertex == second_vertex:
            continue

        if first_vertex > second_vertex:
            first_vertex, second_vertex = second_vertex, first_vertex

        edge = (first_vertex, second_vertex)

        if edge in used_edges:
            continue

        weight = random_generator.randint(1, 100)
        adjacency_list[first_vertex].append((second_vertex, weight))
        adjacency_list[second_vertex].append((first_vertex, weight))
        used_edges.add(edge)

    return adjacency_list


class CountingMinHeap(MinHeap):
    """A MinHeap that counts its operations. Used only in an untimed run."""

    def __init__(self, number_of_vertices):
        MinHeap.__init__(self, number_of_vertices)
        self.extract_min_count = 0
        self.decrease_key_count = 0
        self.swap_count = 0

    def swap(self, first, second):
        self.swap_count = self.swap_count + 1
        MinHeap.swap(self, first, second)

    def extract_min(self):
        self.extract_min_count = self.extract_min_count + 1
        return MinHeap.extract_min(self)

    def decrease_key(self, vertex, new_key):
        self.decrease_key_count = self.decrease_key_count + 1
        MinHeap.decrease_key(self, vertex, new_key)


def count_heap_operations(graph):
    """Run Dijkstra once with a counting heap and return its counters."""
    created_heaps = []

    def make_counting_heap(number_of_vertices):
        heap = CountingMinHeap(number_of_vertices)
        created_heaps.append(heap)
        return heap

    dijkstra_with_heap(graph, 0, heap_class=make_counting_heap)
    heap = created_heaps[0]

    # Inserting the starting vertices causes no swaps: the source has key 0
    # and every other key is infinity. So every swap counted here happens
    # inside extract_min or decrease_key.
    return heap.extract_min_count, heap.decrease_key_count, heap.swap_count


def measure_dijkstra(graph):
    """Return the average running time for Dijkstra's algorithm."""
    measured_times = []

    # One untimed warm-up run, so the first measurement is not slowed down
    # by Python allocating memory for the first time.
    dijkstra_with_heap(graph, 0)

    for repeat in range(NUMBER_OF_REPEATS):
        start_time = time.perf_counter()
        distances, previous = dijkstra_with_heap(graph, 0)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        measured_times.append(elapsed_time)

    total_time = 0

    for measured_time in measured_times:
        total_time = total_time + measured_time

    average_time = total_time / len(measured_times)
    return average_time


def theoretical_work(number_of_vertices, number_of_edges):
    """Return (V + E) log2 V, the quantity the theory says time grows with."""
    return (number_of_vertices + number_of_edges) * math.log2(number_of_vertices)


def record(results, experiment, graph, number_of_edges, average_time):
    """Store one measurement and print it."""
    number_of_vertices = len(graph)
    work = theoretical_work(number_of_vertices, number_of_edges)
    extract_count, decrease_count, swap_count = count_heap_operations(graph)

    result = {
        "experiment": experiment,
        "vertices": number_of_vertices,
        "edges": number_of_edges,
        "average_time_seconds": average_time,
        "time_per_unit_work": average_time / work,
        "extract_min_calls": extract_count,
        "decrease_key_calls": decrease_count,
        "heap_swaps": swap_count,
    }
    results.append(result)

    print(experiment, "V =", number_of_vertices, "E =", number_of_edges)
    print("Average time =", round(average_time, 6), "seconds,",
          "decrease_key calls =", decrease_count)


def run_experiments():
    """Run the three experiments, then return all measurements."""
    random_generator = random.Random(RANDOM_SEED)
    results = []

    # Experiments 1 and 2 use exactly the same settings, seed and graph
    # generator as part (a). The matrix is converted to adjacency lists before
    # timing starts, so both parts are timed on identical graphs.

    # Experiment 1: increase V while keeping density near 25%.
    vertex_counts = [100, 200, 400, 600, 800]

    for number_of_vertices in vertex_counts:
        maximum_edges = number_of_vertices * (number_of_vertices - 1) // 2
        number_of_edges = maximum_edges // 4
        matrix = make_random_connected_graph(
            number_of_vertices,
            number_of_edges,
            random_generator,
        )
        graph = matrix_to_adjacency_list(matrix)
        average_time = measure_dijkstra(graph)
        record(results, "vary_vertices", graph, number_of_edges, average_time)

    # Experiment 2: keep V fixed at 500 while increasing E.
    fixed_vertex_count = 500
    maximum_edges = fixed_vertex_count * (fixed_vertex_count - 1) // 2
    densities = [0.01, 0.10, 0.25, 0.50, 0.90]

    for density in densities:
        number_of_edges = int(maximum_edges * density)
        matrix = make_random_connected_graph(
            fixed_vertex_count,
            number_of_edges,
            random_generator,
        )
        graph = matrix_to_adjacency_list(matrix)
        average_time = measure_dijkstra(graph)
        record(results, "vary_edges", graph, number_of_edges, average_time)

    # Experiment 3: large sparse graphs with E = 5V.
    # An adjacency matrix for V = 50,000 would need 2.5 billion entries,
    # but adjacency lists only need O(V + E) space.
    sparse_vertex_counts = [1000, 2000, 5000, 10000, 20000, 50000]

    for number_of_vertices in sparse_vertex_counts:
        number_of_edges = 5 * number_of_vertices
        graph = make_random_connected_adjacency_list(
            number_of_vertices,
            number_of_edges,
            random_generator,
        )
        average_time = measure_dijkstra(graph)
        record(results, "sparse_vary_vertices", graph, number_of_edges, average_time)

    return results


def save_results(results):
    """Write measurements to a CSV file."""
    RESULTS_FOLDER.mkdir(exist_ok=True)

    column_names = [
        "experiment",
        "vertices",
        "edges",
        "average_time_seconds",
        "time_per_unit_work",
        "extract_min_calls",
        "decrease_key_calls",
        "heap_swaps",
    ]

    with RESULTS_FILE.open("w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(results)


def results_for(results, experiment):
    """Return only the measurements from one experiment."""
    selected = []

    for result in results:
        if result["experiment"] == experiment:
            selected.append(result)

    return selected


def plot_with_theory(selected, x_column, x_label, title, file_name):
    """
    Plot measured times, plus a (V + E) log V curve scaled to the same size.

    The scaling factor is chosen from the largest measurement, so the two
    lines can be compared by shape.
    """
    x_values = []
    times = []
    work_values = []

    for result in selected:
        x_values.append(result[x_column])
        times.append(result["average_time_seconds"])
        work_values.append(theoretical_work(result["vertices"], result["edges"]))

    scale = times[-1] / work_values[-1]
    predicted_times = []

    for work in work_values:
        predicted_times.append(work * scale)

    plt.figure()
    plt.plot(x_values, times, marker="o", label="Measured time")
    plt.plot(x_values, predicted_times, linestyle="--", label="c (V + E) log V")
    plt.xlabel(x_label)
    plt.ylabel("Average time (seconds)")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_FOLDER / file_name, dpi=200)
    plt.close()


def make_plots(results):
    """Create one graph for each experiment."""
    plot_with_theory(
        results_for(results, "vary_vertices"),
        "vertices",
        "Number of vertices, V (density about 25%)",
        "Adjacency lists + min-heap: running time as V increases",
        "part_b_time_vs_vertices.png",
    )

    plot_with_theory(
        results_for(results, "vary_edges"),
        "edges",
        "Number of edges, E (V = 500)",
        "Adjacency lists + min-heap: running time as E increases",
        "part_b_time_vs_edges.png",
    )

    plot_with_theory(
        results_for(results, "sparse_vary_vertices"),
        "vertices",
        "Number of vertices, V (E = 5V)",
        "Adjacency lists + min-heap: large sparse graphs",
        "part_b_time_sparse.png",
    )


if __name__ == "__main__":
    experiment_results = run_experiments()
    save_results(experiment_results)
    make_plots(experiment_results)

    print()
    print("Results saved in:", RESULTS_FOLDER)
