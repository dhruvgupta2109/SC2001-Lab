import random
import unittest

from sorting_algo import generate_random_array, hybrid_sort, original_merge_sort


class SortingAlgorithmTests(unittest.TestCase):
    def test_algorithms_sort_representative_inputs(self):
        cases = [
            [],
            [1],
            [2, 1],
            [1, 1, 1],
            [3, 1, 2, 1],
            list(range(20)),
            list(range(19, -1, -1)),
        ]

        rng = random.Random(42)
        cases.extend([[rng.randint(1, 20) for _ in range(50)] for _ in range(20)])

        for case in cases:
            expected = sorted(case)

            for threshold in (1, 2, 5, 16):
                data = case.copy()
                hybrid_sort(data, 0, len(data) - 1, threshold, [0])
                self.assertEqual(data, expected)

            data = case.copy()
            original_merge_sort(data, 0, len(data) - 1, [0])
            self.assertEqual(data, expected)

    def test_hybrid_sort_rejects_non_positive_threshold(self):
        with self.assertRaises(ValueError):
            hybrid_sort([1], 0, 0, 0, [0])
        with self.assertRaises(ValueError):
            hybrid_sort([1], 0, 0, 1.5, [0])

    def test_generated_values_are_inclusive_and_in_range(self):
        random.seed(42)
        data = generate_random_array(1_000, max_value=10)
        self.assertTrue(all(1 <= value <= 10 for value in data))


if __name__ == "__main__":
    unittest.main()
