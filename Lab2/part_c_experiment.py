"""Part (c): time parts (a) and (b) on the same machine and the same graphs.

Comparing timings taken on different computers is not fair, because one
machine can simply be faster than another. This script runs both
implementations here, one after the other, on identical graphs, and saves:

- results/part_c_results.csv
- results/part_c.png
"""

import csv
import random
import time
from pathlib import Path

import matplotlib.pyplot as plt

from part_a_experiment import make_random_connected_graph
from part_a_matrix_array import dijkstra
from part_b_list_heap import dijkstra_with_heap, matrix_to_adjacency_list


RANDOM_SEED = 42
NUMBER_OF_REPEATS = 5
FIXED_VERTEX_COUNT = 500
DENSITIES = [0.01, 0.10, 0.25, 0.50, 0.75, 0.90, 1.00]

THIS_FOLDER = Path(__file__).resolve().parent
RESULTS_FOLDER = THIS_FOLDER / "results"
RESULTS_FILE = RESULTS_FOLDER / "part_c_results.csv"
VERTEX_RESULTS_FILE = RESULTS_FOLDER / "part_c_vary_vertices.csv"
VERTEX_COUNTS = [100, 200, 400, 600, 800]
PLOT_FILE = RESULTS_FOLDER / "part_c.png"


def average_time(function, graph):
    """Run once to warm up, then return the average of several timed runs."""
    function(graph, 0)
    total_time = 0

    for repeat in range(NUMBER_OF_REPEATS):
        start_time = time.perf_counter()
        function(graph, 0)
        end_time = time.perf_counter()
        total_time = total_time + (end_time - start_time)

    return total_time / NUMBER_OF_REPEATS


def run_experiment():
    """Time both parts on the same graphs as the density increases."""
    random_generator = random.Random(RANDOM_SEED)
    maximum_edges = FIXED_VERTEX_COUNT * (FIXED_VERTEX_COUNT - 1) // 2
    results = []

    for density in DENSITIES:
        number_of_edges = int(maximum_edges * density)
        matrix = make_random_connected_graph(
            FIXED_VERTEX_COUNT,
            number_of_edges,
            random_generator,
        )
        adjacency_list = matrix_to_adjacency_list(matrix)

        time_part_a = average_time(dijkstra, matrix)
        time_part_b = average_time(dijkstra_with_heap, adjacency_list)

        result = {
            "density_percent": int(density * 100),
            "vertices": FIXED_VERTEX_COUNT,
            "edges": number_of_edges,
            "part_a_seconds": time_part_a,
            "part_b_seconds": time_part_b,
            "a_divided_by_b": time_part_a / time_part_b,
        }
        results.append(result)

        if time_part_a < time_part_b:
            faster = "part (a)"
        else:
            faster = "part (b)"

        print(
            "density", str(int(density * 100)) + "%",
            " E =", number_of_edges,
            " (a) =", round(time_part_a, 5),
            " (b) =", round(time_part_b, 5),
            " faster:", faster,
        )

    return results


def run_vertex_experiment():
    """Time both parts on the same graphs as V increases (density about 25%)."""
    random_generator = random.Random(RANDOM_SEED)
    results = []

    for number_of_vertices in VERTEX_COUNTS:
        maximum_edges = number_of_vertices * (number_of_vertices - 1) // 2
        number_of_edges = maximum_edges // 4
        matrix = make_random_connected_graph(
            number_of_vertices,
            number_of_edges,
            random_generator,
        )
        adjacency_list = matrix_to_adjacency_list(matrix)

        time_part_a = average_time(dijkstra, matrix)
        time_part_b = average_time(dijkstra_with_heap, adjacency_list)

        results.append({
            "vertices": number_of_vertices,
            "edges": number_of_edges,
            "part_a_seconds": time_part_a,
            "part_b_seconds": time_part_b,
            "a_divided_by_b": time_part_a / time_part_b,
        })

        print(
            "V =", number_of_vertices,
            " E =", number_of_edges,
            " (a) =", round(time_part_a, 6),
            " (b) =", round(time_part_b, 6),
        )

    return results


def save_results(results, file_path=RESULTS_FILE):
    RESULTS_FOLDER.mkdir(exist_ok=True)
    column_names = list(results[0].keys())

    with file_path.open("w", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(results)


def make_plot(results):
    densities = []
    times_a = []
    times_b = []

    for result in results:
        densities.append(result["density_percent"])
        times_a.append(result["part_a_seconds"])
        times_b.append(result["part_b_seconds"])

    plt.figure(figsize=(8, 5))
    plt.plot(densities, times_a, marker="o", color="red", label="Part (a): Matrix + Array PQ")
    plt.plot(densities, times_b, marker="s", color="blue", label="Part (b): List + Min-Heap PQ")
    plt.title("Dijkstra runtime vs graph density (|V| = 500, same machine, same graphs)")
    plt.xlabel("Graph density (%)")
    plt.ylabel("Average time (seconds)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.savefig(PLOT_FILE, dpi=300, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    experiment_results = run_experiment()
    save_results(experiment_results)
    make_plot(experiment_results)
    print()
    vertex_results = run_vertex_experiment()
    save_results(vertex_results, VERTEX_RESULTS_FILE)
    print()
    print("Saved", VERTEX_RESULTS_FILE)
    print("Saved", RESULTS_FILE)
    print("Saved", PLOT_FILE)
