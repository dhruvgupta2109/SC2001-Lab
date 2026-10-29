"""Part (3): bottom-up DP for the unbounded knapsack problem.

P(c) is the largest profit achievable with total weight at most c.
Every object type can be used any number of times.
"""


def build_dp_table(capacity, weights, profits):
    """Return the profit table and one best object choice for every capacity.

    dp[c] holds P(c). choice[c] holds the type of one object used in an
    optimal packing for c, or None if no object fits. Types are numbered
    from 0. If several choices give the same profit, keep the first type.
    """
    if not isinstance(capacity, int) or capacity < 0:
        raise ValueError("The capacity must be a non-negative integer.")
    if len(weights) != len(profits):
        raise ValueError("weights and profits must have the same length.")
    for i in range(len(weights)):
        if (not isinstance(weights[i], int) or weights[i] <= 0
                or not isinstance(profits[i], int) or profits[i] <= 0):
            raise ValueError("Every weight and profit must be a positive integer.")

    # Packing nothing gives profit 0, including when no object fits.
    dp = [0] * (capacity + 1)
    choice = [None] * (capacity + 1)

    # All dependencies c - weights[i] are smaller than c, so they are ready.
    for c in range(1, capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= c:
                candidate = profits[i] + dp[c - weights[i]]

                if candidate > dp[c]:
                    dp[c] = candidate
                    choice[c] = i

    return dp, choice


def max_profit_bottom_up(capacity, weights, profits):
    """Return P(capacity), computed iteratively without recursive calls."""
    dp, choice = build_dp_table(capacity, weights, profits)
    return dp[capacity]


def reconstruct_counts(capacity, weights, choice):
    """Recover object counts using the choices from build_dp_table.

    Pass the same capacity and weights used to build choice. Stop when
    nothing fits; any remaining capacity can be left unused.
    """
    counts = [0] * len(weights)
    remaining = capacity

    while choice[remaining] is not None:
        object_type = choice[remaining]
        counts[object_type] += 1
        remaining -= weights[object_type]

    return counts
