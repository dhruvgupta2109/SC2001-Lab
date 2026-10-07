import matplotlib.pyplot as plt

densities = [1, 10, 25, 50, 90]
time_part_a = [0.01085, 0.01175, 0.01262, 0.01418, 0.01490]
time_part_b = [0.00247, 0.00619, 0.00894, 0.01795, 0.03126]

plt.figure(figsize=(8, 5))
plt.plot(densities, time_part_a, marker='o', label='Part (a): Matrix + Array PQ', color='red')
plt.plot(densities, time_part_b, marker='s', label='Part (b): List + Min-Heap PQ', color='blue')

plt.title('Dijkstra Runtime vs Graph Density (|V| = 500)')
plt.xlabel('Graph Density (%)')
plt.ylabel('Execution Time (seconds)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

plt.savefig('part_c.png', dpi=300, bbox_inches='tight')
plt.show()
