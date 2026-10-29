"""Correctness checks for Dhruv's bottom-up implementation and packings."""

from itertools import product
import random
import unittest

from part_1_recursive import max_profit_recursive
from part_3_bottom_up import (
    build_dp_table,
    max_profit_bottom_up,
    reconstruct_counts,
)


def enumerate_best_profit(capacity, weights, profits):
    """Independent reference: enumerate every feasible vector of counts."""
    best_profit = 0
    count_ranges = [range(capacity // weight + 1) for weight in weights]

    for counts in product(*count_ranges):
        weight = sum(counts[i] * weights[i] for i in range(len(weights)))
        if weight <= capacity:
            profit = sum(counts[i] * profits[i] for i in range(len(profits)))
            best_profit = max(best_profit, profit)

    return best_profit


class TestBottomUpKnapsack(unittest.TestCase):
    def check_packing(self, capacity, weights, profits, dp, choice):
        counts = reconstruct_counts(capacity, weights, choice)
        self.assertEqual(len(counts), len(weights))
        self.assertTrue(all(count >= 0 for count in counts))
        weight = sum(counts[i] * weights[i] for i in range(len(weights)))
        profit = sum(counts[i] * profits[i] for i in range(len(profits)))
        self.assertLessEqual(weight, capacity)
        self.assertEqual(profit, dp[capacity])

    def test_required_examples(self):
        examples = [
            (16, [4, 5, 8], [7, 6, 9], 28, [4, 0, 0]),
            (12, [5, 6, 7], [7, 6, 9], 16, [1, 0, 1]),
        ]
        for capacity, weights, profits, expected, expected_counts in examples:
            with self.subTest(capacity=capacity):
                dp, choice = build_dp_table(capacity, weights, profits)
                self.assertEqual(dp[capacity], expected)
                self.assertEqual(max_profit_bottom_up(capacity, weights, profits),
                                 expected)
                self.assertEqual(reconstruct_counts(capacity, weights, choice),
                                 expected_counts)
                self.check_packing(capacity, weights, profits, dp, choice)

    def test_zero_capacity_nothing_fits_and_empty_types(self):
        for capacity, weights, profits in [
            (0, [4, 5, 8], [7, 6, 9]),
            (3, [4, 5, 8], [7, 6, 9]),
            (10, [], []),
        ]:
            with self.subTest(capacity=capacity, weights=weights):
                dp, choice = build_dp_table(capacity, weights, profits)
                self.assertEqual(dp, [0] * (capacity + 1))
                self.check_packing(capacity, weights, profits, dp, choice)

    def test_unlimited_supply_and_unused_capacity(self):
        # Three copies fit, even though a single type is supplied.
        dp, choice = build_dp_table(10, [3], [5])
        self.assertEqual(dp[10], 15)
        self.assertEqual(reconstruct_counts(10, [3], choice), [3])
        self.check_packing(10, [3], [5], dp, choice)

    def test_greedy_profit_per_weight_can_fail(self):
        # Type 0 has the best ratio, but two type 1 objects give more profit.
        self.assertEqual(max_profit_bottom_up(8, [3, 4], [5, 6]), 12)

    def test_ties_keep_first_type(self):
        dp, choice = build_dp_table(8, [4, 4], [7, 7])
        self.assertEqual(reconstruct_counts(8, [4, 4], choice), [2, 0])
        self.check_packing(8, [4, 4], [7, 7], dp, choice)

    def test_large_capacity_without_recursion(self):
        self.assertEqual(max_profit_bottom_up(5000, [1], [2]), 10000)

    def test_every_entry_and_packing_against_brute_force(self):
        rng = random.Random(42)
        for case in range(100):
            number_of_types = rng.randint(1, 4)
            weights = [rng.randint(1, 10) for _ in range(number_of_types)]
            profits = [rng.randint(1, 20) for _ in range(number_of_types)]
            capacity = rng.randint(0, 20)
            dp, choice = build_dp_table(capacity, weights, profits)

            for c in range(capacity + 1):
                with self.subTest(case=case, capacity=c):
                    self.assertEqual(dp[c], enumerate_best_profit(c, weights, profits))
                    self.assertEqual(dp[c], max_profit_recursive(c, weights, profits))
                    self.check_packing(c, weights, profits, dp, choice)

    def test_invalid_input_is_rejected(self):
        invalid_inputs = [
            (-1, [4], [7]),
            (1.5, [4], [7]),
            (10, [4, 5], [7]),
            (10, [0], [7]),
            (10, [-4], [7]),
            (10, [4.5], [7]),
            (10, [4], [0]),
            (10, [4], [-7]),
            (10, [4], [7.5]),
        ]
        for capacity, weights, profits in invalid_inputs:
            with self.subTest(capacity=capacity, weights=weights, profits=profits):
                with self.assertRaises(ValueError):
                    max_profit_bottom_up(capacity, weights, profits)


if __name__ == "__main__":
    unittest.main()
