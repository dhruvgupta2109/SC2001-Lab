"""Run the empirical time-complexity experiments for part (a)."""

import csv
import random
import time
from pathlib import Path

import matplotlib.pyplot as plt

from part_a_matrix_array import dijkstra


RANDOM_SEED = 42
NUMBER_OF_REPEATS = 5

THIS_FOLDER = Path(__file__).resolve().parent
RESULTS_FOLDER = THIS_FOLDER / "results"
RESULTS_FILE = RESULTS_FOLDER / "part_a_results.csv"


def make_random_connected_graph(number_of_vertices, number_of_edges, random_generator):
    """Create a connected, undirected matrix with exactly the requested edges."""
    smallest_edge_count = number_of_vertices - 1
    largest_edge_count = number_of_vertices * (number_of_vertices - 1) // 2

    if number_of_edges < smallest_edge_count:
        raise ValueError("A connected graph needs at least V - 1 edges.")

    if number_of_edges > largest_edge_count:
        raise ValueError("The requested graph has too many edges.")

    matrix = []

    for row_number in range(number_of_vertices):
        row = []

        for column_number in range(number_of_vertices):
            row.append(None)

        matrix.append(row)

    # First add a chain. This guarantees that the graph is connected.
    used_edges = set()

    for vertex in range(number_of_vertices - 1):
        next_vertex = vertex + 1
        weight = random_generator.randint(1, 100)

        matrix[vertex][next_vertex] = weight
        matrix[next_vertex][vertex] = weight
        used_edges.add((vertex, next_vertex))

    # List every other possible undirected edge.
    available_edges = []

    for first_vertex in range(number_of_vertices):
        for second_vertex in range(first_vertex + 1, number_of_vertices):
            edge = (first_vertex, second_vertex)

            if edge not in used_edges:
                available_edges.append(edge)

    random_generator.shuffle(available_edges)

    extra_edges_needed = number_of_edges - smallest_edge_count

    for edge_number in range(extra_edges_needed):
        first_vertex, second_vertex = available_edges[edge_number]
        weight = random_generator.randint(1, 100)

        matrix[first_vertex][second_vertex] = weight
        matrix[second_vertex][first_vertex] = weight

    return matrix


def measure_dijkstra(graph):
    """Return the average running time for Dijkstra's algorithm."""
    measured_times = []

    for repeat in range(NUMBER_OF_REPEATS):
        start_time = time.perf_counter()
        distances, previous = dijkstra(graph, 0)
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        measured_times.append(elapsed_time)

    total_time = 0

    for measured_time in measured_times:
        total_time = total_time + measured_time

    average_time = total_time / len(measured_times)
    return average_time


def run_experiments():
    """Vary V and E separately, then return all measurements."""
    random_generator = random.Random(RANDOM_SEED)
    results = []

    # Experiment 1: increase V while keeping density near 25%.
    vertex_counts = [100, 200, 400, 600, 800]

    for number_of_vertices in vertex_counts:
        maximum_edges = number_of_vertices * (number_of_vertices - 1) // 2
        number_of_edges = maximum_edges // 4
        graph = make_random_connected_graph(
            number_of_vertices,
            number_of_edges,
            random_generator,
        )
        average_time = measure_dijkstra(graph)

        result = {
            "experiment": "vary_vertices",
            "vertices": number_of_vertices,
            "edges": number_of_edges,
            "average_time_seconds": average_time,
        }
        results.append(result)

        print("V =", number_of_vertices, "E =", number_of_edges)
        print("Average time =", round(average_time, 6), "seconds")

    # Experiment 2: keep V fixed while increasing E.
    fixed_vertex_count = 500
    maximum_edges = fixed_vertex_count * (fixed_vertex_count - 1) // 2
    densities = [0.01, 0.10, 0.25, 0.50, 0.90]

    for density in densities:
        number_of_edges = int(maximum_edges * density)
        graph = make_random_connected_graph(
            fixed_vertex_count,
            number_of_edges,
            random_generator,
        )
        average_time = measure_dijkstra(graph)

        result = {
            "experiment": "vary_edges",
            "vertices": fixed_vertex_count,
            "edges": number_of_edges,
            "average_time_seconds": average_time,
        }
        results.append(result)

        print("V =", fixed_vertex_count, "E =", number_of_edges)
        print("Average time =", round(average_time, 6), "seconds")

    return results


def save_results(results):
    """Write measurements to a CSV file."""
    RESULTS_FOLDER.mkdir(exist_ok=True)

    column_names = [
        "experiment",
        "vertices",
        "edges",
        "average_time_seconds",
    ]

    with RESULTS_FILE.open("w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(results)


def make_plots(results):
    """Create one graph for each experiment."""
    vertex_results = []
    edge_results = []

    for result in results:
        if result["experiment"] == "vary_vertices":
            vertex_results.append(result)
        else:
            edge_results.append(result)

    vertex_counts = []
    vertex_times = []

    for result in vertex_results:
        vertex_counts.append(result["vertices"])
        vertex_times.append(result["average_time_seconds"])

    plt.figure()
    plt.plot(vertex_counts, vertex_times, marker="o")
    plt.xlabel("Number of vertices, V")
    plt.ylabel("Average time (seconds)")
    plt.title("Adjacency matrix + array: running time as V increases")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_FOLDER / "part_a_time_vs_vertices.png", dpi=200)
    plt.close()

    edge_counts = []
    edge_times = []

    for result in edge_results:
        edge_counts.append(result["edges"])
        edge_times.append(result["average_time_seconds"])

    plt.figure()
    plt.plot(edge_counts, edge_times, marker="o")
    plt.xlabel("Number of edges, E")
    plt.ylabel("Average time (seconds)")
    plt.title("Adjacency matrix + array: running time as E increases")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(RESULTS_FOLDER / "part_a_time_vs_edges.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    experiment_results = run_experiments()
    save_results(experiment_results)
    make_plots(experiment_results)

    print()
    print("Results saved in:", RESULTS_FOLDER)
