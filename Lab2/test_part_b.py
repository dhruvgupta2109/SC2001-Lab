"""Correctness tests for the part (b) implementation."""

import random
import unittest

from part_a_matrix_array import dijkstra
from part_b_list_heap import (
    INFINITY,
    MinHeap,
    dijkstra_with_heap,
    make_path,
    matrix_to_adjacency_list,
)


class TestMinHeap(unittest.TestCase):
    def test_extract_min_returns_sorted_order(self):
        keys = [5, 3, 8, 1, 9, 2, 7]
        heap = MinHeap(len(keys))

        for vertex in range(len(keys)):
            heap.insert(vertex, keys[vertex])

        extracted = []

        while not heap.is_empty():
            vertex, key = heap.extract_min()
            extracted.append(key)

        self.assertEqual(extracted, sorted(keys))

    def test_decrease_key_moves_vertex_to_front(self):
        heap = MinHeap(4)

        for vertex in range(4):
            heap.insert(vertex, 10 + vertex)

        heap.decrease_key(3, 1)

        self.assertEqual(heap.extract_min(), (3, 1))
        self.assertFalse(heap.contains(3))


class TestDijkstraListHeap(unittest.TestCase):
    def test_example_graph(self):
        graph = [
            [(1, 10), (2, 3)],
            [(2, 1), (3, 2)],
            [(1, 4), (3, 8), (4, 2)],
            [(4, 7)],
            [(3, 9)],
        ]

        distances, previous = dijkstra_with_heap(graph, 0)

        self.assertEqual(distances, [0, 7, 3, 9, 5])
        self.assertEqual(make_path(previous, 0, 3), [0, 2, 1, 3])

    def test_unreachable_vertex(self):
        graph = [
            [(1, 5)],
            [],
            [],
        ]

        distances, previous = dijkstra_with_heap(graph, 0)

        self.assertEqual(distances[2], INFINITY)
        self.assertEqual(make_path(previous, 0, 2), [])

    def test_zero_weight_edge(self):
        graph = [
            [(1, 0)],
            [],
        ]

        distances, previous = dijkstra_with_heap(graph, 0)

        self.assertEqual(distances, [0, 0])
        self.assertEqual(make_path(previous, 0, 1), [0, 1])

    def test_negative_edge_is_rejected(self):
        graph = [
            [(1, -1)],
            [],
        ]

        with self.assertRaises(ValueError):
            dijkstra_with_heap(graph, 0)

    def test_matches_part_a_on_random_graphs(self):
        random_generator = random.Random(2001)

        for trial in range(50):
            number_of_vertices = random_generator.randint(1, 30)
            matrix = []

            for row_number in range(number_of_vertices):
                row = []

                for column_number in range(number_of_vertices):
                    if row_number != column_number and random_generator.random() < 0.3:
                        row.append(random_generator.randint(0, 20))
                    else:
                        row.append(None)

                matrix.append(row)

            source = random_generator.randrange(number_of_vertices)
            expected_distances, unused = dijkstra(matrix, source)
            actual_distances, unused = dijkstra_with_heap(
                matrix_to_adjacency_list(matrix),
                source,
            )

            self.assertEqual(actual_distances, expected_distances)


if __name__ == "__main__":
    unittest.main()
