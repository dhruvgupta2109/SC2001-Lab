"""Part (1): a recursive definition of P(C) for the knapsack problem.

There are n types of objects. An object of type i has weight weights[i] and
profit profits[i]. There is an unlimited supply of every type.

P(C) is the largest total profit that fits in a knapsack of capacity C:

    P(C) = 0                                         if weights[i] > C for every i
    P(C) = max over every i with weights[i] <= C of (profits[i] + P(C - weights[i]))
"""


def check_input(capacity, weights, profits):
    """Raise ValueError if the problem description is not valid."""
    if len(weights) != len(profits):
        raise ValueError("weights and profits must have the same length.")

    if capacity < 0:
        raise ValueError("The capacity cannot be negative.")

    for i in range(len(weights)):
        if weights[i] <= 0 or profits[i] <= 0:
            raise ValueError("Every weight and profit must be a positive integer.")


def max_profit_recursive(capacity, weights, profits, memo=None):
    """
    Return P(capacity) by following the recursive definition directly.

    The supply of every type is unlimited, so after we place an object of
    type i, every type is still available. The only thing that changes is
    the remaining capacity, which is why P needs only one parameter.

    memo stores every P(c) that has already been worked out, so each
    subproblem is solved once instead of many times.
    """
    if memo is None:
        check_input(capacity, weights, profits)
        memo = {}

    if capacity in memo:
        return memo[capacity]

    # Base case: if no object fits, nothing can be packed, so the profit is 0.
    best_profit = 0

    # Recursive case: try every object that fits as the "first" object, then
    # pack the remaining capacity as well as possible.
    for i in range(len(weights)):
        if weights[i] <= capacity:
            remaining_capacity = capacity - weights[i]
            profit = profits[i] + max_profit_recursive(
                remaining_capacity, weights, profits, memo
            )

            if profit > best_profit:
                best_profit = profit

    memo[capacity] = best_profit
    return best_profit


def count_plain_recursive_calls(capacity, weights):
    """
    Count how many calls the recursion makes when it does NOT remember
    answers. Comparing this with the number of distinct subproblems shows
    why dynamic programming helps.
    """
    calls = 1

    for i in range(len(weights)):
        if weights[i] <= capacity:
            calls = calls + count_plain_recursive_calls(capacity - weights[i], weights)

    return calls


def print_example():
    """Print P(C) for C = 0 to 15 using the weights and profits from part (2)."""
    weights = [4, 5, 8]
    profits = [7, 6, 9]
    capacity = 15

    print("Weights:", weights)
    print("Profits:", profits)
    print()

    memo = {}
    max_profit_recursive(capacity, weights, profits, memo)

    for c in range(capacity + 1):
        if c in memo:
            print("P(" + str(c) + ") =", memo[c])

    print()
    print("Answer: P(" + str(capacity) + ") =", memo[capacity])
    print("Distinct subproblems solved:", len(memo))
    print("Calls made by plain recursion without memo:",
          count_plain_recursive_calls(capacity, weights))


if __name__ == "__main__":
    print_example()
