# genetic-algorithms

#  Genetic Algorithm for Traveling Salesman Problem (TSP)

A Python implementation of a Genetic Algorithm to approximate solutions for the Traveling Salesman Problem (TSP), one of the most famous NP-hard problems.

## Problem Description

The Traveling Salesman Problem (TSP): Given a list of cities and distances between them, find the shortest possible route that visits each city exactly once and returns to the starting city. This is NP-hard, so we use a genetic algorithm to find near-optimal solutions.

### Example with 10 Cities
| City | Coordinates |
|------|-------------|
| 1 | (60, 200) |
| 2 | (180, 200) |
| 3 | (80, 180) |
| 4 | (140, 180) |
| 5 | (20, 160) |
| 6 | (100, 160) |
| 7 | (200, 160) |
| 8 | (140, 140) |
| 9 | (40, 120) |
| 10 | (100, 120) |

## ⚙️ Algorithm Analysis

### Time Complexity
- **Overall:** O(g·p·n) where:
  - g = number of generations
  - p = population size
  - n = number of cities

### Space Complexity
- **Population Storage:** O(p·n)

## Genetic Algorithm Components

### 1. Initialization
Create random population of routes (permutations of city indices)

### 2. Fitness Evaluation
Fitness = 1 / total_route_distance (shorter routes = higher fitness)

### 3. Selection
Roulette wheel selection - better routes have higher chance of being selected

### 4. Crossover
Ordered Crossover (OX) - preserves ordering of cities from parents

### 5. Mutation
Swap mutation - randomly swaps two cities in the route

### 6. Elitism
Best routes are automatically preserved in next generation

## Code Example

```python
# Create sample cities
cities = [
    (60, 200), (180, 200), (80, 180), (140, 180), (20, 160),
    (100, 160), (200, 160), (140, 140), (40, 120), (100, 120)
]

# Initialize genetic algorithm
ga = GeneticAlgorithmTSP(
    cities=cities,
    pop_size=50,
    mutation_rate=0.02,
    elite_size=10,
    generations=100
)

# Run evolution
best_route = ga.evolve()

# Print result
print(f"Best distance: {ga.best_distance:.2f}")
