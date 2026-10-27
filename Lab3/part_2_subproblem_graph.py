"""Part (2): draw the subproblem graph for P(15).

Each vertex is a subproblem P(c). There is an edge from P(c) to
P(c - w_i) whenever an object of type i fits, because computing P(c)
directly needs the answer to P(c - w_i).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch

from part_1_recursive import max_profit_recursive


LAB_DIR = Path(__file__).resolve().parent
RESULTS_DIR = LAB_DIR / "results"

WEIGHTS = [4, 5, 8]
PROFITS = [7, 6, 9]
CAPACITY = 15

# One colour per object type, so you can see which object each edge uses.
EDGE_COLOURS = ["#1E5AA8", "#D9822B", "#2E8B57"]


def build_subproblem_graph(capacity, weights):
    """
    Return the vertices and edges reachable from P(capacity).

    vertices is a list of capacities, largest first.
    edges is a list of (from_capacity, to_capacity, object_type).
    """
    vertices = []
    edges = []
    to_visit = [capacity]
    seen = {capacity}

    while len(to_visit) > 0:
        current = to_visit.pop(0)
        vertices.append(current)

        for i in range(len(weights)):
            if weights[i] <= current:
                smaller = current - weights[i]
                edges.append((current, smaller, i))

                if smaller not in seen:
                    seen.add(smaller)
                    to_visit.append(smaller)

    vertices.sort(reverse=True)
    return vertices, edges


def find_levels(vertices, edges):
    """
    Give each vertex a level so that every edge points downwards.

    A vertex's level is the length of the longest path to it from the top
    vertex. Every edge goes to a smaller capacity, so visiting vertices from
    largest to smallest capacity is a valid order.
    """
    level = {}
    for vertex in vertices:
        level[vertex] = 0

    for vertex in vertices:
        for start, end, object_type in edges:
            if start == vertex and level[end] < level[vertex] + 1:
                level[end] = level[vertex] + 1

    return level


def find_positions(vertices, level):
    """Spread the vertices of each level evenly across the picture."""
    rows = {}
    for vertex in vertices:
        rows.setdefault(level[vertex], []).append(vertex)

    positions = {}
    gap_x = 2.4
    gap_y = 2.6

    for row_number, row in rows.items():
        row.sort(reverse=True)
        width = (len(row) - 1) * gap_x

        for index in range(len(row)):
            x = index * gap_x - width / 2
            y = -row_number * gap_y
            positions[row[index]] = (x, y)

    return positions


def draw_graph(vertices, edges, values, output_path):
    """Draw the graph and save it as a PNG file."""
    level = find_levels(vertices, edges)
    positions = find_positions(vertices, level)
    radius = 0.62

    fig, ax = plt.subplots(figsize=(11, 9.5))

    for start, end, object_type in edges:
        x1, y1 = positions[start]
        x2, y2 = positions[end]

        # Edges that skip a level are curved so they do not pass through
        # the vertices in between.
        levels_skipped = level[end] - level[start] - 1
        if levels_skipped == 0:
            curve = 0.0
        elif x2 <= x1:
            curve = 0.32
        else:
            curve = -0.32

        # Start and finish each arrow on the edge of the circles, not at
        # their centres, so the arrowhead is not hidden by a circle.
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        step_x = (x2 - x1) / distance
        step_y = (y2 - y1) / distance
        start_point = (x1 + step_x * radius, y1 + step_y * radius)
        end_point = (x2 - step_x * radius, y2 - step_y * radius)

        arrow = FancyArrowPatch(
            start_point, end_point,
            connectionstyle="arc3,rad=" + str(curve),
            arrowstyle="-|>", mutation_scale=20,
            shrinkA=0, shrinkB=1,
            color=EDGE_COLOURS[object_type], linewidth=1.8, zorder=4,
        )
        ax.add_patch(arrow)

    for vertex in vertices:
        x, y = positions[vertex]
        no_object_fits = all(edge[0] != vertex for edge in edges)

        if no_object_fits:
            face_colour = "#EEEEEE"
        else:
            face_colour = "#DCE6F7"

        ax.add_patch(Circle((x, y), radius, facecolor=face_colour,
                            edgecolor="#1A1A2E", linewidth=1.6, zorder=2))
        ax.text(x, y + 0.13, "P(" + str(vertex) + ")", ha="center", va="center",
                fontsize=13, fontweight="bold", color="#1A1A2E", zorder=3)
        ax.text(x, y - 0.24, "= " + str(values[vertex]), ha="center", va="center",
                fontsize=10.5, color="#444444", zorder=3)

    legend_items = []
    for i in range(len(WEIGHTS)):
        label = ("type " + str(i) + ":  w = " + str(WEIGHTS[i])
                 + ",  p = " + str(PROFITS[i]))
        legend_items.append(Line2D([0], [0], color=EDGE_COLOURS[i], linewidth=2.5,
                                   label=label))
    legend_items.append(Line2D([0], [0], marker="o", color="white",
                               markerfacecolor="#EEEEEE", markeredgecolor="#1A1A2E",
                               markersize=14, label="base case: no object fits"))

    ax.legend(handles=legend_items, loc="lower right", fontsize=10.5, frameon=True,
              title="Edge P(c) -> P(c - w_i) uses object type i", title_fontsize=10.5)

    all_x = [positions[v][0] for v in vertices]
    all_y = [positions[v][1] for v in vertices]
    ax.set_xlim(min(all_x) - 1.6, max(all_x) + 1.6)
    ax.set_ylim(min(all_y) - 2.6, max(all_y) + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Subproblem graph for P(" + str(CAPACITY) + ")   (w = "
                 + str(WEIGHTS) + ", p = " + str(PROFITS) + ")",
                 fontsize=14, fontweight="bold")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main():
    memo = {}
    max_profit_recursive(CAPACITY, WEIGHTS, PROFITS, memo)

    vertices, edges = build_subproblem_graph(CAPACITY, WEIGHTS)

    print("Subproblem graph for P(" + str(CAPACITY) + ")")
    print("Weights:", WEIGHTS, " Profits:", PROFITS)
    print()
    print("Vertices:", len(vertices), " Edges:", len(edges))
    print()

    for vertex in vertices:
        children = []
        for start, end, object_type in edges:
            if start == vertex:
                children.append("P(" + str(end) + ") [type " + str(object_type) + "]")

        if len(children) == 0:
            children_text = "none (base case, P = 0)"
        else:
            children_text = ", ".join(children)

        print("P(" + str(vertex) + ") = " + str(memo[vertex]) + "  ->  " + children_text)

    RESULTS_DIR.mkdir(exist_ok=True)
    output_path = RESULTS_DIR / "part_2_subproblem_graph_P15.png"
    draw_graph(vertices, edges, memo, output_path)
    print()
    print("Saved", output_path)


if __name__ == "__main__":
    main()
