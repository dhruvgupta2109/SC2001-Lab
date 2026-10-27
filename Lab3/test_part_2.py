"""Checks for the part (2) subproblem graph."""

import unittest

from part_2_subproblem_graph import build_subproblem_graph, find_levels


class TestSubproblemGraph(unittest.TestCase):
    def setUp(self):
        self.vertices, self.edges = build_subproblem_graph(15, [4, 5, 8])

    def test_vertices(self):
        self.assertEqual(self.vertices, [15, 11, 10, 7, 6, 5, 3, 2, 1, 0])

    def test_edges(self):
        expected = {
            (15, 11, 0), (15, 10, 1), (15, 7, 2),
            (11, 7, 0), (11, 6, 1), (11, 3, 2),
            (10, 6, 0), (10, 5, 1), (10, 2, 2),
            (7, 3, 0), (7, 2, 1),
            (6, 2, 0), (6, 1, 1),
            (5, 1, 0), (5, 0, 1),
        }
        self.assertEqual(len(self.edges), 15)
        self.assertEqual(set(self.edges), expected)

    def test_every_edge_goes_to_a_smaller_capacity(self):
        # This is why the graph has no cycles, so a bottom-up order exists.
        for start, end, object_type in self.edges:
            self.assertLess(end, start)

    def test_levels_point_downwards(self):
        level = find_levels(self.vertices, self.edges)

        for start, end, object_type in self.edges:
            self.assertGreater(level[end], level[start])


if __name__ == "__main__":
    unittest.main()
