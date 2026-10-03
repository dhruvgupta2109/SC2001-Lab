"""Correctness tests for the part (a) implementation."""

import unittest

from part_a_matrix_array import INFINITY, dijkstra, make_path


class TestDijkstraMatrixArray(unittest.TestCase):
    def test_example_graph(self):
        graph = [
            [None, 10,   3, None, None],
            [None, None, 1,    2, None],
            [None,   4, None,  8,    2],
            [None, None, None, None, 7],
            [None, None, None,   9, None],
        ]

        distances, previous = dijkstra(graph, 0)

        self.assertEqual(distances, [0, 7, 3, 9, 5])
        self.assertEqual(make_path(previous, 0, 3), [0, 2, 1, 3])

    def test_unreachable_vertex(self):
        graph = [
            [None, 5, None],
            [None, None, None],
            [None, None, None],
        ]

        distances, previous = dijkstra(graph, 0)

        self.assertEqual(distances[2], INFINITY)
        self.assertEqual(make_path(previous, 0, 2), [])

    def test_zero_weight_edge(self):
        graph = [
            [None, 0],
            [None, None],
        ]

        distances, previous = dijkstra(graph, 0)

        self.assertEqual(distances, [0, 0])
        self.assertEqual(make_path(previous, 0, 1), [0, 1])

    def test_negative_edge_is_rejected(self):
        graph = [
            [None, -1],
            [None, None],
        ]

        with self.assertRaises(ValueError):
            dijkstra(graph, 0)


if __name__ == "__main__":
    unittest.main()
