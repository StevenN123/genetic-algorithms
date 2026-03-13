"""
Genetic Algorithm for Traveling Salesman Problem (TSP)
Author: Steven N
Description: Evolutionary algorithm to approximate solutions for the NP-hard TSP
"""

import random  # Import random module for generating random numbers and shuffling
import math    # Import math module for mathematical operations like sqrt


class City:
    """Represents a city with x,y coordinates"""
    
    def __init__(self, x, y):
        """Initialize a city with x and y coordinates"""
        self.x = x  # Store the x-coordinate of the city
        self.y = y  # Store the y-coordinate of the city
    
    def distance_to(self, other):
        """Calculate Euclidean distance to another city"""
        # Calculate the difference in x coordinates
        dx = self.x - other.x
        # Calculate the difference in y coordinates
        dy = self.y - other.y
        # Return the straight-line distance using Pythagorean theorem
        return math.sqrt(dx*dx + dy*dy)


class Route:
    """Represents a TSP route (order of cities to visit)"""
    
    def __init__(self, cities, route=None):
        """Initialize a route with a list of cities and optional route order"""
        # Store the list of all cities
        self.cities = cities
        
        # If no route is provided, create a random one
        if route is None:
            # Create a list of city indices [0, 1, 2, ..., n-1]
            self.route = list(range(len(cities)))
            # Shuffle the list to create a random order
            random.shuffle(self.route)
        else:
            # Use the provided route
            self.route = route
        
        # Set up the cache for distance (None means not calculated yet)
        self.distance = None
        # Set up the cache for fitness (None means not calculated yet)
        self.fitness = None
    
    def calculate_distance(self):
        """Calculate total distance of the route"""
        # Return cached distance if already calculated
        if self.distance is not None:
            return self.distance
        
        # Setting up total distance to 0
        total = 0
        # Get the number of cities in the route
        n = len(self.route)
        
        # Loop through each city in the route
        for i in range(n):
            # Get the current city using its index from the route
            from_city = self.cities[self.route[i]]
            # Get the next city (wrap around to first for return trip)
            to_city = self.cities[self.route[(i + 1) % n]]
            # Add the distance between current and next city to total
            total += from_city.distance_to(to_city)
        
        # Cache the calculated distance
        self.distance = total
        # Return the total distance
        return total
    
    def calculate_fitness(self):
        """Calculate fitness (higher is better - inverse of distance)"""
        # Return cached fitness if already calculated
        if self.fitness is not None:
            return self.fitness
        # Fitness is inverse of distance (shorter route = higher fitness)
        self.fitness = 1 / self.calculate_distance()
        # Return the calculated fitness
        return self.fitness


class GeneticAlgorithmTSP:
    """Genetic Algorithm for Traveling Salesman Problem"""
    
    def __init__(self, cities, pop_size=100, mutation_rate=0.01, 
                 elite_size=20, generations=500):
        """Initialize the genetic algorithm with parameters"""
        
        # Convert input cities to City objects if they are tuples
        self.cities = []
        for c in cities:
            # Check if the city is a tuple (x, y)
            if isinstance(c, tuple):
                # Create a City object from the tuple
                self.cities.append(City(c[0], c[1]))
            else:
                # City is already a City object
                self.cities.append(c)
        
        # Store algorithm parameters
        self.pop_size = pop_size          # Population size
        self.mutation_rate = mutation_rate # Probability of mutation
        self.elite_size = elite_size       # Number of best routes to keep
        self.generations = generations      # Number of generations to run
        self.num_cities = len(self.cities)  # Number of cities
        
        # Initialize empty population list
        self.population = []
        # Initialize best route as None
        self.best_route = None
        # Set up the best distance as infinity
        self.best_distance = float('inf')
    
    def create_individual(self):
        """Create a random route (individual)"""
        # Create a list of city indices [0, 1, 2, ..., n-1]
        route = list(range(self.num_cities))
        # Shuffle the list to create a random order
        random.shuffle(route)
        # Create and return a Route object
        return Route(self.cities, route)
    
    def create_population(self):
        """Create initial population of random routes"""
        # Generate pop_size random individuals
        self.population = [self.create_individual() for _ in range(self.pop_size)]
        
        # Find the best route in initial population
        for route in self.population:
            # Calculate distance for this route
            dist = route.calculate_distance()
            # Check if this is better than current best
            if dist < self.best_distance:
                # Update best distance
                self.best_distance = dist
                # Update best route
                self.best_route = route
        
        # Print the initial best distance
        print(f"Initial best distance: {self.best_distance:.2f}")
    
    def rank_routes(self):
        """Rank routes by fitness (higher fitness = better)"""
        # Create dictionary to store fitness for each route
        fitness = {}
        # Loop through all routes in population
        for i, route in enumerate(self.population):
            # Calculate and store fitness for route i
            fitness[i] = route.calculate_fitness()
        # Sort routes by fitness (highest first) and return
        return sorted(fitness.items(), key=lambda x: x[1], reverse=True)
    
    def selection(self, ranked_pop):
        """Select parents using roulette wheel selection"""
        # List to store selected parent indexes
        results = []
        # Calculate total fitness of all routes
        total_fitness = sum(ranked_pop[i][1] for i in range(len(ranked_pop)))
        
        # Select parents (excluding elite count)
        for _ in range(len(ranked_pop) - self.elite_size):
            # Pick a random point on the wheel
            pick = random.uniform(0, total_fitness)
            current = 0
            # Find which route corresponds to the picked point
            for i in range(len(ranked_pop)):
                current += ranked_pop[i][1]
                if current > pick:
                    # Add this route index to selection results
                    results.append(ranked_pop[i][0])
                    break
        # Return list of selected parent indexes
        return results
    
    def mating_pool(self, selection_results):
        """Create mating pool from selected parents"""
        # Create empty pool list
        pool = []
        # Loop through selected indexes
        for i in range(len(selection_results)):
            # Get the index of the selected parent
            index = selection_results[i]
            # Add the corresponding route to the mating pool
            pool.append(self.population[index])
        # Return the mating pool
        return pool
    
    def crossover(self, parent1, parent2):
        """Ordered Crossover (OX) for TSP"""
        # Get number of cities
        n = self.num_cities
        
        # Choose random start and end positions for the part
        start = random.randint(0, n - 1)
        end = random.randint(0, n - 1)
        
        # Ensure start <= end (swap if needed)
        if start > end:
            start, end = end, start
        
        # Create child route with -1 placeholders
        child_route = [-1] * n
        
        # Copy the segment from parent1 to child
        for i in range(start, end + 1):
            child_route[i] = parent1.route[i]
        
        # Fill remaining positions with parent2's cities in order
        j = 0
        for i in range(n):
            # Check if this position is still empty
            if child_route[i] == -1:
                # Find next city in parent2 not already in child
                while parent2.route[j] in child_route:
                    j += 1
                # Add this city to the child
                child_route[i] = parent2.route[j]
                j += 1
        
        # Create and return a new Route object
        return Route(self.cities, child_route)
    
    def mutate(self, route):
        """Swap mutation - swap two random cities in the route"""
        # Loop through each position in the route
        for _ in range(len(route.route)):
            # Check if mutation should occur at this position
            if random.random() < self.mutation_rate:
                # Choose two random positions to swap
                i = random.randint(0, self.num_cities - 1)
                j = random.randint(0, self.num_cities - 1)
                # Swap the cities at positions i and j
                route.route[i], route.route[j] = route.route[j], route.route[i]
        
        # Reset cached values since route has changed
        route.distance = None
        route.fitness = None
        
        # Return the route
        return route
    
    def next_generation(self):
        """Create the next generation"""
        # Rank current population by fitness
        ranked = self.rank_routes()
        
        # Keep elite individuals (best routes)
        elite_indices = [ranked[i][0] for i in range(self.elite_size)]
        elite_population = [self.population[i] for i in elite_indices]
        
        # Select parents and create mating pool
        selection_results = self.selection(ranked)
        pool = self.mating_pool(selection_results)
        
        # Create children through crossover and mutation
        children = []
        # Generate enough children to fill the rest of population
        while len(children) < self.pop_size - self.elite_size:
            # Select two random parents from mating pool
            parent1 = random.choice(pool)
            parent2 = random.choice(pool)
            # Apply crossover to create child
            child = self.crossover(parent1, parent2)
            # Apply mutation to child
            child = self.mutate(child)
            # Add child to children list
            children.append(child)
        
        # New population = elites + children
        self.population = elite_population + children
        
        # Update best route if found
        for route in self.population:
            # Calculate distance for this route
            dist = route.calculate_distance()
            # Check if this is better than current best
            if dist < self.best_distance:
                # Update best distance
                self.best_distance = dist
                # Update best route
                self.best_route = route
                # Print new best found
                print(f"  🏆 New best: {dist:.2f}")
    
    def evolve(self):
        """Run the genetic algorithm"""
        # Create initial population
        self.create_population()
        
        # Run for specified number of generations
        for gen in range(1, self.generations + 1):
            # Create next generation
            self.next_generation()
            
            # Print progress every 50 generations
            if gen % 50 == 0:
                print(f"Generation {gen}: Best = {self.best_distance:.2f}")
        
        # Return the best route found
        return self.best_route


def create_sample_cities():
    """Create a sample set of cities for testing"""
    # Return a list of 10 city coordinates
    return [
        (60, 200), (180, 200), (80, 180), (140, 180), (20, 160),
        (100, 160), (200, 160), (140, 140), (40, 120), (100, 120)
    ]


# Example usage
if __name__ == "__main__":
    # Print header
    print("=" * 60)
    print("GENETIC ALGORITHM FOR TRAVELING SALESMAN PROBLEM")
    print("=" * 60)
    
    # Create sample cities
    cities = create_sample_cities()
    
    # Print city coordinates
    print("\nCities:")
    for i, (x, y) in enumerate(cities):
        print(f"  City {i+1}: ({x}, {y})")
    
    # Initialize genetic algorithm
    ga = GeneticAlgorithmTSP(
        cities=cities,           # List of cities
        pop_size=50,             # Population size
        mutation_rate=0.02,       # Mutation rate
        elite_size=10,            # Number of elites to keep
        generations=100           # Number of generations
    )
    
    # Run evolution
    print("\n" + "=" * 60)
    print("EVOLVING POPULATION")
    print("=" * 60)
    best = ga.evolve()
    
    # Print final results
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    print(f"Best distance: {ga.best_distance:.2f}")
    print(f"Best route: {best.route}")
