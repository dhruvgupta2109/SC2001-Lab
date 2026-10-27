"""Correctness tests for the part (1) recursive definition."""

import random
import unittest

from part_1_recursive import count_plain_recursive_calls, max_profit_recursive


def brute_force_profit(capacity, weights, profits):
    """
    Try every possible count of every object type and keep the best total
    profit that fits. This is slow but obviously correct, so it is a good
    reference for small inputs.
    """
    best_profit = 0

    def try_counts(type_index, remaining_capacity, profit_so_far):
        nonlocal best_profit

        if type_index == len(weights):
            if profit_so_far > best_profit:
                best_profit = profit_so_far
            return

        largest_count = remaining_capacity // weights[type_index]

        for count in range(largest_count + 1):
            try_counts(
                type_index + 1,
                remaining_capacity - count * weights[type_index],
                profit_so_far + count * profits[type_index],
            )

    try_counts(0, capacity, 0)
    return best_profit


class TestRecursiveDefinition(unittest.TestCase):
    def test_part_2_example(self):
        weights = [4, 5, 8]
        profits = [7, 6, 9]

        self.assertEqual(max_profit_recursive(15, weights, profits), 21)

    def test_values_used_in_part_4(self):
        # These are the two cases asked for in part (4). The bottom-up
        # algorithm should give the same answers.
        self.assertEqual(max_profit_recursive(16, [4, 5, 8], [7, 6, 9]), 28)
        self.assertEqual(max_profit_recursive(12, [5, 6, 7], [7, 6, 9]), 16)

    def test_nothing_fits(self):
        self.assertEqual(max_profit_recursive(0, [4, 5, 8], [7, 6, 9]), 0)
        self.assertEqual(max_profit_recursive(3, [4, 5, 8], [7, 6, 9]), 0)

    def test_single_type_is_repeated(self):
        # With unlimited supply, the best packing is as many copies as fit.
        self.assertEqual(max_profit_recursive(10, [3], [5]), 15)

    def test_matches_brute_force_on_random_inputs(self):
        rng = random.Random(42)

        for _ in range(200):
            number_of_types = rng.randint(1, 4)
            weights = [rng.randint(1, 10) for _ in range(number_of_types)]
            profits = [rng.randint(1, 20) for _ in range(number_of_types)]
            capacity = rng.randint(0, 30)

            self.assertEqual(
                max_profit_recursive(capacity, weights, profits),
                brute_force_profit(capacity, weights, profits),
            )

    def test_memo_avoids_repeated_work(self):
        memo = {}
        max_profit_recursive(15, [4, 5, 8], [7, 6, 9], memo)

        self.assertEqual(len(memo), 10)
        self.assertEqual(count_plain_recursive_calls(15, [4, 5, 8]), 20)

    def test_invalid_input_is_rejected(self):
        with self.assertRaises(ValueError):
            max_profit_recursive(10, [4, 5], [7])
        with self.assertRaises(ValueError):
            max_profit_recursive(-1, [4], [7])
        with self.assertRaises(ValueError):
            max_profit_recursive(10, [0], [7])


if __name__ == "__main__":
    unittest.main()
